# -*- coding: utf-8 -*-
import locale
from operator import attrgetter
import os
from datetime import date, timedelta
import datetime
from random import randint

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count
from django.utils.datastructures import SortedDict
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from simplejson import dumps, loads

from attestation.forms import RequestForm
from attestation.models import *
from libs.ODTFile import ODTFile, ODTFileError
from settings import MEDIA_URL, MEDIA_ROOT


def request_form(request):
    """
    Request form for non-authorized clients
    """
    title = _('Send attestation request')
    custom_styles = ['smoothness/jquery-ui-1.8.23.custom.css', 'chosen.css']
    custom_scripts = ['libs/chosen.jquery.min.js']

    if request.method == 'POST':
        data = request.POST.copy()
        form = RequestForm(data)
        if form.is_valid():
            data = form.cleaned_data.copy()
            r = Request()
            if request.POST.get('id'):
                r = Request.objects.get(id=request.POST.get('id'))

            fn = data.get('first_name')
            fn = fn.strip().capitalize()
            r.first_name = fn

            ln = data.get('last_name')
            ln = ln.strip().capitalize()
            r.last_name = ln

            mn = data.get('middle_name')
            mn = mn.strip().capitalize()
            r.middle_name = mn
            r.birth_date = data.get('birth_date')

            r.email = data.get('email')
            r.official_email = data.get('official_email')
            r.post = data.get('post')
            r.discipline = data.get('discipline')
            r.post_date = data.get('post_date')
            r.qualification = data.get('qualification')
            r.with_qualification = data.get('with_qualification')
            r.expiration_date = data.get('expiration_date')
            r.presence = data.get('presence')
            r.territory = data.get('territory')
            r.organization = data.get('organization')
            r.organization_name = data.get('organization_name')
            r.organization_experience = data.get('organization_experience')
            r.post_experience = data.get('post_experience')
            r.academic_title = data.get('academic_title')
            r.experience = data.get('experience')
            r.pedagogical_experience = data.get('ped_experience')
            r.genitive = data.get('genitive')
            r.organization_type = data.get('organization_type')
            res = data.get('results')
            if res[-1] == '.':
                res = res[0:-1]
            r.results = res.strip()
            tr = data.get('trainings')
            if tr and tr[-1] == '.':
                tr = tr[0:-1]
            r.trainings = tr.strip()

            r.phone = data.get('phone')

            if data.get('simple_doc'):
                r.doc_for_simple = data['simple_doc']
            r.save()

            r.degrees.clear()
            r.achievements.clear()
            for d in data.get('degrees', []):
                r.degrees.add(d)
            for a in data.get('achievements', []):
                r.achievements.add(a)

            e = Education()
            if request.POST.get('edu1_id'):
                e = Education.objects.get(id=request.POST.get('edu1_id'))
            e.institution = data.get('edu_institution')
            e.speciality = data.get('edu_speciality')
            e.qualification = data.get('edu_qualification')
            e.diploma_year = data.get('edu_diploma_year')
            e.request = r
            e.save()

            ei2 = data.get('edu_institution2')
            if ei2:
                e2 = Education()
                if request.POST.get('edu2_id'):
                    try:
                        e2 = Education.objects.get(id=request.POST.get('edu2_id'))
                    except ObjectDoesNotExist:
                        pass
                e2.request = r
                e2.institution = ei2
                e2.speciality = data.get('edu_speciality2')
                e2.qualification = data.get('edu_qualification2')
                e2.diploma_year = data.get('edu_diploma_year2')
                e2.save()

            if request.POST.get('edu2_id') and not ei2:
                try:
                    e2 = Education.objects.get(id=request.POST.get('edu2_id'))
                    e2.delete()
                except ObjectDoesNotExist:
                    pass

            return HttpResponseRedirect(reverse('attestation.views.request', args=[r.secret_code]))
    else:
        form = RequestForm()
        id = request.GET.get("id")
        qid = request.GET.get("q")
        if id:
            try:
                r = Request.objects.get(id=id)

                if not RequestFlow.objects.filter(request=r) or request.user.is_authenticated():
                    data = {"first_name": r.first_name, "last_name": r.last_name, "middle_name": r.middle_name,
                            "email": r.email, "post": r.post, "qualification": r.qualification,
                            "with_qualification": r.with_qualification, "expiration_date": r.expiration_date,
                            "presence": r.presence, "territory": r.territory, "organization": r.organization,
                            "organization_name": r.organization_name,
                            "organization_experience": r.organization_experience,
                            "post_experience": r.post_experience, "degrees": r.degrees.all(),
                            "academic_title": r.academic_title,
                            "experience": r.experience, "ped_experience": r.pedagogical_experience,
                            "results": r.results,
                            "trainings": r.trainings, "phone": r.phone, 'birth_date': r.birth_date,
                            "achievements": r.achievements.all(), "post_date": r.post_date, "genitive": r.genitive,
                            "discipline": r.discipline, 'simple_doc': r.doc_for_simple,
                            "organization_type": r.organization_type, "official_email": r.official_email}

                    educations = Education.objects.filter(request=r)
                    if educations:
                        data["edu_institution"] = educations[0].institution
                        data["edu_speciality"] = educations[0].speciality
                        data["edu_qualification"] = educations[0].qualification
                        data["edu_diploma_year"] = educations[0].diploma_year
                        edu1_id = educations[0].pk
                        if len(educations) > 1:
                            data["edu_institution2"] = educations[1].institution
                            data["edu_speciality2"] = educations[1].speciality
                            data["edu_qualification2"] = educations[1].qualification
                            data["edu_diploma_year2"] = educations[1].diploma_year
                            edu2_id = educations[1].pk

                    form.initial = data
                else:
                    id = None

            except ObjectDoesNotExist:
                id = None
                pass
        else:
            form.initial = {'qualification': qid}

    template = loader.get_template("request_form.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


def request(request, rcode):
    """
    Print request sheet. User can confirm request and set status 'new'.
    Or user can return to request form and change request data.
    """
    title = _('Request')

    year = date.today().year
    month = date.today().month

    r = get_object_or_404(Request, secret_code=rcode)
    edu = Education.objects.filter(request=r)

    flows = r.requestflow_set.all()

    d = datetime.date.today()
    if flows:
        d = flows[0].date

    commission = CertifyingCommission.objects.filter(creation_date__lte=d).filter(
        expiration_date__gte=d)
    if commission:
        commission = commission[0]

    status = RequestStatus.objects.filter(is_new=True)[0]
    rf = RequestFlow.objects.filter(request=r, status=status)
    if rf:
        year = rf[0].date.year
        month = rf[0].date.month

    if month >= 10:
        year += 1

    if request.method == "POST":
        if not r.requestflow_set.count():
            flow = RequestFlow()
            flow.request = r
            flow.status = status
            flow.save()
            r.status = status
            r.save()

    template = loader.get_template("request.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def request_by_id(request, rid):
    """
    Print request sheet. User can confirm request and set status 'new'.
    Or user can return to request form and change request data.
    """
    title = _('Request')

    year = date.today().year
    month = date.today().month

    r = get_object_or_404(Request, id=rid)
    edu = Education.objects.filter(request=r)

    flows = RequestFlow.objects.filter(request=r)

    d = datetime.date.today()
    if flows:
        d = flows[0].date

    commission = CertifyingCommission.objects.filter(creation_date__lte=d).filter(
        expiration_date__gte=d)
    if commission:
        commission = commission[0]

    status = RequestStatus.objects.filter(is_new=True)[0]
    rf = RequestFlow.objects.filter(request=r, status=status)
    if rf:
        year = rf[0].date.year
        month = rf[0].date.month

    if month >= 10:
        year += 1

    if request.method == "POST":
        if not r.requestflow_set.count():
            flow = RequestFlow()
            flow.request = r
            flow.status = status
            flow.save()
            r.status = status
            r.save()

    template = loader.get_template("request.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def request_details(request, rid):
    req = get_object_or_404(Request, id=rid)
    if request.method == "POST":
        data = request.POST.copy()
        req.recomendations = data.get('recomendations', None)
        req.decision = data.get('decision', None)
        req.notes = data.get('notes', None)
        req.number_of_members = data.get('number', None)
        req.agree = data.get('agree', 0)
        req.disagree = data.get('disagree', 0)
        req.retrain = data.get('retrain', 0)
        ad = data.get('attestation_date', None)
        adate = None
        if ad:
            try:
                adate = datetime.datetime.strptime(ad, "%d.%m.%Y")
            except ValueError:
                pass
        req.attestation_date = adate
        req.order_number = data.get('order_number', "")
        if req.order_number == "":
            req.order_number = None
        od = data.get('order_date', None)
        odate = None
        if od:
            try:
                odate = datetime.datetime.strptime(od, "%d.%m.%Y")
            except ValueError:
                pass
        req.order_date = odate
        req.save()

    title = _('Request detail')
    custom_scripts = ['libs/jquery.dataTables.min.js']
    custom_styles = ['jquery.dataTables.css', 'smoothness/jquery-ui-1.8.23.custom.css']

    statuses = req.requestflow_set.select_related('status').all()
    all_statuses = RequestStatus.objects.all()
    all_experts = Expert.objects.select_related('area', 'territory').filter(not_active=False)
    eir = ExpertInRequest.objects.select_related('expert', 'expert__area').filter(request=req)

    template = loader.get_template("request_details.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def set_current_status(request_, rid):
    req = get_object_or_404(Request, id=rid)
    if request_.method == 'POST':
        data = request_.POST.copy()
        last_flow = req.requestflow_set.order_by('-date')[0]
        if 0 < data.get('set_status', -1) != last_flow.status.pk:
            try:
                status = RequestStatus.objects.get(id=data.get('set_status', -1))
                last_flow.status = status
                last_flow.save()
                last_flow.request.status = status
                last_flow.request.save()
            except ObjectDoesNotExist:
                pass
        if 0 < data.get('new_status', -1) != last_flow.status.pk:
            try:
                status = RequestStatus.objects.get(id=data.get('new_status', -1))
                RequestFlow.objects.create(request=req, status=status)
                req.status = status
                req.save()
            except ObjectDoesNotExist:
                pass

        if data.get('documents', None) and req.doc_date is None:
            req.doc_date = datetime.date.today()
            req.save()

            msg = EmailMultiAlternatives(
                u'Документы по Вашему заявлению получены'.encode('utf-8'),
                u"""
В системе аттестации педагогических работников ХМАО-Югры зарегистрирован факт получения
оригиналов документов по Вашему заявлению (№ %s).
                """.encode('utf-8') % req.pk,
                'att@iro86.ru', [req.email]
            )
            msg.attach_alternative(
                u"""
<html><p>В системе аттестации педагогических работников ХМАО-Югры зарегистрирован факт получения
оригиналов документов по Вашему заявлению (№ %s).</p></html>
                """.encode('utf-8'), 'text/html'
            )
            msg.send(fail_silently=not DEBUG)

    return HttpResponseRedirect(reverse('attestation.views.request_details', args=[rid]))


@login_required
def sheet(request, rid):
    title = _('Attestation sheet')

    req = get_object_or_404(Request, id=rid)

    educations = req.education_set.all()
    commission = None

    # get commission for request date
    rf = req.requestflow_set.filter(status__is_expertise_results_received=True)
    if rf:
        commission = CertifyingCommission.objects.filter(creation_date__lte=rf[0].date).filter(
            expiration_date__gte=rf[0].date)
        if commission:
            commission = commission[0]
            number_of_members = commission.members.count()

    if commission:
        territory_member = commission.members.filter(territory=req.territory)
        if territory_member:
            territory_member = territory_member[0]

    experts = req.expertinrequest_set.all()
    first_stage_avg = 0
    second_stage_avg = 0
    first_count = 0
    second_count = 0
    for e in experts:
        if e.first_grade:
            first_count += 1
            first_stage_avg += e.first_grade
        if e.second_grade:
            second_count += 1
            second_stage_avg += e.second_grade

    if first_count > 0 and second_count > 0:
        first_stage_avg /= first_count
        second_stage_avg /= second_count

    total_grade = first_stage_avg + second_stage_avg
    template = loader.get_template("sheet.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
@csrf_exempt
def save_grades(request):
    if request.method != 'POST':
        return HttpResponse("GET")
    post = request.POST.copy()

    d = post.get('data', '{}')
    data = loads(d)

    if isinstance(data, dict):
        for k in data.keys():
            grade = data[k]
            id = grade['id']
            stage = grade['stage']
            value = grade['value']
            try:
                exp = ExpertInRequest.objects.get(id=int(id))
                if int(stage) == 1:
                    try:
                        exp.first_grade = float(value)
                    except:
                        exp.first_grade = None
                else:
                    try:
                        exp.second_grade = float(value)
                    except:
                        exp.second_grade = None
                exp.save()
            except ValueError:
                pass
            except ObjectDoesNotExist:
                return HttpResponse("NOTFOUND")
        return HttpResponse('OK')
    return HttpResponse('BADTYPE')


@login_required
def assign_experts(request_, rid):
    try:
        r = Request.objects.select_related('territory', 'organization').get(id=rid)
        data = request_.POST.copy()
        experts_pks = data.getlist('experts')
        if len(experts_pks) > 0:
            for eid in experts_pks:
                expert = Expert.objects.get(id=eid)
                ExpertInRequest.objects.get_or_create(request=r, expert=expert)
        else:
            current_date = datetime.datetime.now()
            m = current_date.month
            if 7 <= m <= 12:
                first_september = datetime.datetime(current_date.year, 9, 1)
                first_july = datetime.datetime(current_date.year + 1, 7, 1)
            else:
                first_september = datetime.datetime(current_date.year - 1, 9, 1)
                first_july = datetime.datetime(current_date.year, 7, 1)

            year_requests = [
                f.request for f in RequestFlow.objects.select_related('request').filter(
                    status__is_in_expertise=True, date__gte=first_september, date__lte=first_july
                )
            ]
            counts = {
                e[0]: e[1] for e in
                Expert.objects.filter(
                    not_active=False,
                    expertinrequest__request__in=year_requests
                ).annotate(cnt=Count('request')).values_list('id', 'cnt')
            }
            experts_list = list(Expert.objects.filter(
                organization_type=r.organization_type, organization_type__isnull=False
            ))

            # manual annotation
            for e in experts_list:
                e.cnt = counts.get(e.id, 0)

            experts_list = sorted(experts_list, key=lambda e_: (e_.cnt, randint(0, 1000)), reverse=True)

            assigned_experts_count = ExpertInRequest.objects.filter(request=r).count()

            i = 0
            while assigned_experts_count < 1:
                expert_ = experts_list[i]
                if expert_.cnt <= 30:
                    expert_in_request, created = ExpertInRequest.objects.get_or_create(
                        request=r, expert=expert_, defaults={'auto_assigned': True}
                    )
                    i += 1
                    if created:
                        assigned_experts_count += 1

    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect(reverse('attestation.views.request_details', args=[rid]))


@login_required
def drop_expert(request, rid, eir):
    try:
        e = ExpertInRequest.objects.get(id=eir)
        e.delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(reverse('attestation.views.request_details', args=[rid]))


@login_required
def expert_results(request, rid):
    title = _('Results of work of experts')
    c = RequestContext(request, locals())
    results_date = datetime.date.today()

    try:
        r = Request.objects.get(id=rid)
        c['request'] = r
        child = r.organization != None

        #get config for this request
        rf = RequestFlow.objects.filter(request=r)
        if rf:
            for f in rf:
                if f.status.is_new:
                    conf = Config.objects.filter(start_date__lte=f.date).filter(end_date__gte=f.date) \
                        .filter(category=r.qualification).filter(is_child_organization=child)
                    if conf:
                        c['config'] = conf[0]
                        if (conf[0].first_stage_max_grade is None) or (conf[0].second_stage_max_grade is None):
                            c['max_grade'] = None
                        else:
                            c['max_grade'] = conf[0].first_stage_max_grade + conf[0].second_stage_max_grade
                        c['min_grade'] = conf[0].first_stage_min_grade + conf[0].second_stage_min_grade

        # get experts
        experts = ExpertInRequest.objects.filter(request=r)
        first_count = 0
        second_count = 0
        if len(experts) > 0:
            i = 1
            first_avg = 0
            second_avg = 0
            for e in experts:
                c['exp%s' % i] = e
                i += 1
                if e.first_grade:
                    first_avg += e.first_grade
                    first_count += 1
                if e.second_grade:
                    second_count += 1
                    second_avg += e.second_grade

            c['first_avg_grade'] = first_avg / first_count if first_count else 0
            c['second_avg_grade'] = second_avg / second_count if second_count else 0
            c['result'] = c['first_avg_grade'] + c['second_avg_grade']


    except ObjectDoesNotExist:
        raise Http404

    template = loader.get_template("expert_results.html")

    return HttpResponse(template.render(c))


#@login_required
#@csrf_exempt
#def reassign(request):
#    if request.method != 'POST':
#        return HttpResponse("GET")
#    data = request.POST.copy()
#    try:
#        r = Request.objects.get(id=data.get('rid', 0))
#        e = Expert.objects.get(id=data.get('eid', 0))
#
#        experts_set = Expert.objects.all().annotate(cnt=Count('request')).order_by('cnt')
#        assigned_experts = [eir.expert for eir in ExpertInRequest.objects.filter(request=r)]
#        if len(experts_set) >= 3:
#            eir = ExpertInRequest.objects.get(request=r, expert=e)
#            eir.delete()
#
#            i = 0
#            expert = experts_set[i]
#            while expert in assigned_experts:
#                i += 1
#                if i >= len(experts_set): # for better safety
#                    expert = experts_set[0]
#                    break
#                expert = experts_set[i]
#
#            new_e = ExpertInRequest.objects.create(request=r, expert=expert)
#
#            n = {
#                'first_name': new_e.expert.first_name,
#                'last_name': new_e.expert.last_name,
#                'middle_name': new_e.expert.middle_name,
#                'organization': new_e.expert.organization,
#                'post': new_e.expert.post.name,
#                'id': new_e.expert.pk
#            }
#
#            return HttpResponse(dumps(n), mimetype='text/json')
#
#    except ObjectDoesNotExist:
#        return HttpResponse('NOTFOUND')


@login_required
@cache_page(300)
def requests(request):
    title = _('All requests')
    custom_scripts = ['libs/jquery.dataTables.min.js']
    custom_styles = ['jquery.dataTables.css']

    reqs = {}
    requests_ = Request.objects.select_related(
        'territory', 'organization', 'status', 'qualification',
        'with_qualification', 'post'
    ).filter(status__is_done=False, qualification__for_confirmation=False)

    if request.GET.get('simple'):
        requests_ = requests_.filter(doc_for_simple__isnull=False)
    else:
        requests_ = requests_.filter(doc_for_simple__isnull=True)

    for r in requests_:
        reqs.setdefault(r.status, []).append(r)

    template = loader.get_template("requests.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def mark_as_completed(request):
    title = _('Mark as completed')
    custom_scripts = ['libs/jquery.dataTables.min.js']
    custom_styles = ['jquery.dataTables.css']

    statuses = RequestStatus.objects.filter(is_expertise_results_received=True)

    reqs = {}
    requests_ = Request.objects.select_related(
        'territory', 'organization', 'status', 'qualification',
        'with_qualification', 'post'
    ).filter(status__in=statuses)

    for r in requests_:
        reqs.setdefault(r.status, []).append(r)

    try:
        s = RequestStatus.objects.get(is_done=True)
    except ObjectDoesNotExist:
        s = None
    except MultipleObjectsReturned:
        s = RequestStatus.objects.filter(is_done=True)[0]

    if request.method == 'POST':
        if s:
            for req in reqs.values():
                for r in req:
                    RequestFlow.objects.create(request=r, status=s)
                    r.status = s
                    r.save()
            completed = True
            reqs = {}

    template = loader.get_template("make_completed.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
@cache_page(60)
def completed_requests(request, period=None):
    title = _('All completed requests')
    custom_scripts = ['libs/jquery.dataTables.min.js']
    custom_styles = ['jquery.dataTables.css']

    statuses = RequestStatus.objects.filter(is_done=True)

    unsorted_reqs = {}
    periods = set()
    rfs = RequestFlow.objects.select_related(
        'request', 'request__territory', 'request__organization', 'status', 'request__qualification',
        'request__with_qualification', 'request__post'
    ).distinct('request').order_by('request', '-date')

    if not period:
        aggregation = RequestFlow.objects.filter(status__is_done=True).aggregate(Max('date'))
        if aggregation['date__max']:
            period = aggregation['date__max'].strftime('%Y.%m')

    for flow in rfs:
        st = flow.status
        d = flow.date.strftime('%Y.%m')
        if st in statuses:
            periods.add(d)
            if d != period:
                continue
            if not d in unsorted_reqs.keys():
                unsorted_reqs[d] = []

            unsorted_reqs[d].append(flow.request)

    keys = unsorted_reqs.keys()
    keys.sort(reverse=True)

    reqs = SortedDict((k, unsorted_reqs[k]) for k in keys)
    periods = sorted(periods, reverse=True)

    template = loader.get_template("requests.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@csrf_exempt
@login_required
def next_status(request):
    if request.method != 'POST':
        return HttpResponse("GET")
    data = request.POST.copy()

    rid = data.get('rid', 0)
    if rid:
        try:
            req = Request.objects.get(id=rid)
            flows = RequestFlow.objects.filter(request=req).order_by('-date')
            if flows:
                status = flows[0].status
                if status.next_status:
                    f = RequestFlow.objects.create(request=req, status=status.next_status)
                    req.status = status.next_status
                    req.save()
                    locale.setlocale(locale.LC_TIME, '')
                    resp = {
                        "status": f.status.name,
                        "date": f.date.strftime('%x')
                    }
                    return HttpResponse(dumps(resp), mimetype='text/json')
                else:
                    return HttpResponse('END')
            else:
                return HttpResponse('NOTINFLOW')

        except ObjectDoesNotExist:
            return HttpResponse('NOTFOUND')


def expert_blank(request, rcode, eid):
    title = _('Grade sheet for experts')

    req = get_object_or_404(Request, secret_code=rcode)
    eir = get_object_or_404(ExpertInRequest, id=eid)

    template = loader.get_template("expert_blank.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


#lost
def expert_sheet(request, rcode, eid):
    title = _('Expert sheet')

    req = get_object_or_404(Request, secret_code=rcode)
    eir = get_object_or_404(ExpertInRequest, id=eid)

    criteria = Criterion.objects.select_related().all()
    max = 0
    for c in criteria:
        for i in c.indicator_set.all():
            max += i.cost

    template = loader.get_template("expert_sheet.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


def sort_key(r):
    t = r.territory if r.territory else r.organization.territory
    if t:
        return t.name, r.last_name, r.first_name
    else:
        return u'не указано', r.last_name, r.first_name


def data_for_protocol():
    today = datetime.date.today()

    best = Qualification.objects.get(best=True)
    fst = Qualification.objects.get(first=True)
    confrm = Qualification.objects.get(for_confirmation=True)

    statuses = RequestStatus.objects.exclude(is_new=True).exclude(is_rejected=True).exclude(is_done=True).exclude(
        is_in_expertise=True)

    requests_ = Request.objects.select_related(
        'status', 'qualification', 'territory', 'organization',
        'organization__territory'
    ).filter(status__in=statuses)

    by_q = {}
    terr = set()
    for r in requests_:
        by_q.setdefault(r.qualification, []).append(r)
        terr.add(r.territory)

    commission = CertifyingCommission.objects.select_related('members').filter(
        creation_date__lte=today
    ).filter(
        expiration_date__gte=today
    )
    commission_not_configured = False
    if commission:
        commission = commission[0]
        members = commission.members.all()
    else:
        commission_not_configured = True
        members = CertifyingCommissionMember.objects.all()

    high = sorted(by_q.get(best, []), key=sort_key)
    first = sorted(by_q.get(fst, []), key=sort_key)

    today = datetime.date.today().strftime("%d.%m.%Y")

    return locals()


@login_required
def protocol(request):
    title = _('Protocol')

    custom_scripts = ['libs/chosen.jquery.min.js']
    custom_styles = ['chosen.css']

    pd = data_for_protocol()

    commission_not_configured = pd['commission_not_configured']
    commission = pd['commission']
    members = pd['members']
    high = pd['high']
    first = pd['first']
    terr = pd['terr']
    stat = pd['statuses']

    if request.method == "POST" and not commission_not_configured:
        data = request.POST.copy()

        unpresent_members = []
        members_pk = data.getlist('unpresent')
        for i in members_pk:
            try:
                unpresent_members.append(CertifyingCommissionMember.objects.get(id=i))
            except ObjectDoesNotExist:
                pass

        unpresent_members = sorted(unpresent_members, key=attrgetter('last_name', 'first_name'))
        unpresent_members_text = '\n'.join([m.__unicode__() for m in unpresent_members])

        adm = [commission.vice_chairman, commission.chairman, commission.secretary]

        present_members = [m for m in members if (m not in unpresent_members) and (m not in adm)]
        present_members = sorted(present_members, key=attrgetter('last_name', 'first_name'))
        present_members_text = '\n'.join(m.__unicode__() for m in present_members)

        protocol_date = pd['today']

        high_fail = []
        hf_pk = data.getlist('high-fail')
        for i in hf_pk:
            try:
                r = Request.objects.get(id=i)
                high_fail.append(r)
            except ObjectDoesNotExist:
                pass

        high_fail = sorted(high_fail, key=attrgetter('last_name', 'first_name'))

        first_fail = []
        ff_pk = data.getlist('first-fail')
        for i in ff_pk:
            try:
                r = Request.objects.get(id=i)
                first_fail.append(r)
            except ObjectDoesNotExist:
                pass

        first_fail = sorted(first_fail, key=attrgetter('last_name', 'first_name'))

        highfailtemplate = u"О не соответствии %s требованиям, предъявляемым к высшей квалификационной категории на \
основании пункта ____ Положения об организационных формах и процедурах аттестации педагогических работников \
государственных и муниципальных образовательных учреждений ХМАО–Югры. Голосование: ЗА ____, ПРОТИВ ____.\r"
        firstfailtemplate = u"О не соответствии %s требованиям, предъявляемым к первой квалификационной категории на \
основании пункта ____ Положения об организационных формах и процедурах аттестации педагогических работников \
государственных и муниципальных образовательных учреждений ХМАО–Югры. Голосование: ЗА ____, ПРОТИВ ____.\r"

        highfailtexts = u""
        for r in high_fail:
            highfailtexts += highfailtemplate % r.genitive

        firstfailtexts = u""
        for r in first_fail:
            firstfailtexts += firstfailtemplate % r.genitive

        try:
            file = ODTFile(os.path.join(MEDIA_ROOT, 'odt/protocol.odt'))
            file.fill_template({
                "protocol_date": protocol_date,
                "present_members_text": present_members_text,
                "unpresent_membrs_text": unpresent_members_text,
                "chairman": commission.chairman.__unicode__() if commission.chairman else "",
                "vice_chairman": commission.vice_chairman.__unicode__() if commission.vice_chairman else "",
                "secretary": commission.secretary.__unicode__(),
                "hcount": str(len(high)),
                "hfail": str(len(high_fail)),
                "hdone": str(len(high) - len(high_fail)),
                "requestscount": str(len(high) + len(first)),
                "territorycount": str(len(terr)),
                "fcount": str(len(first)),
                "ffail": str(len(first_fail)),
                "fdone": str(len(first) - len(first_fail)),
                "highfailtexts": highfailtexts,
                "firstfailtexts": firstfailtexts,
            })
            file.save(os.path.join(MEDIA_ROOT, 'generated/protocol_%s.doc' % protocol_date))
            file_link = os.path.join(MEDIA_URL, 'generated/protocol_%s.doc' % protocol_date)
        except ODTFileError:
            generator_error = 'File generation error'

    template = loader.get_template("protocol.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@csrf_exempt
@login_required
def order(request):
    if request.method == "POST":

        today = datetime.date.today().strftime("%d.%m.%Y")

        try:
            fl = ODTFile(os.path.join(MEDIA_ROOT, 'odt/order.odt'))
            fl.fill_template({
                "attdate": today,
                "expdate": (datetime.datetime.today() + timedelta(5 * 365)).strftime("%d.%m.%Y"),
            })
            fl.save(os.path.join(MEDIA_ROOT, 'generated/order_%s.doc' % today))
            file_link = os.path.join(MEDIA_URL, 'generated/order_%s.doc' % today)
            return HttpResponse(file_link)
        except ODTFileError:
            return HttpResponse('GENERROR')

    return HttpResponse("GET")


@csrf_exempt
@login_required
def addition(request):
    if request.method == "POST":
        data = request.POST.copy()

        pd = data_for_protocol()
        high = pd['high']
        first = pd['first']
        today = pd['today']

        # TODO sort_key
        # TODO shrink spaces
        # TODO full post

        high_fail = []
        hf_pk = data.getlist('high-fail[]')
        for i in hf_pk:
            try:
                r = Request.objects.get(id=i)
                high_fail.append(r)
                try:
                    high.remove(r)
                except ValueError:
                    pass
            except ObjectDoesNotExist:
                pass

        first_fail = []
        ff_pk = data.getlist('first-fail[]')
        for i in ff_pk:
            try:
                r = Request.objects.get(id=i)
                first_fail.append(r)
                try:
                    first.remove(r)
                except ValueError:
                    pass
            except ObjectDoesNotExist:
                pass

        high_fail.extend(first_fail)
        high_first_fail = sorted(high_fail, key=sort_key)
        high_first_fail_text = ''
        index = 1
        for hf in high_first_fail:
            org = hf.organization
            if not org:
                org = "%s, %s" % (hf.organization_name, hf.territory)
            else:
                org = org.name
            if hf.discipline:
                post = hf.post.name + " " + hf.discipline
            else:
                post = hf.post.name
            high_first_fail_text += '%s. %s, %s, %s\r' % (index, hf.fio(), post, ' '.join(org.split()))
            index += 1

        high_text = ''
        index = 1
        for h in high:
            org = h.organization
            if not org:
                org = "%s, %s" % (h.organization_name, h.territory)
            else:
                org = org.name
            if h.discipline:
                post = h.post.name + " " + h.discipline
            else:
                post = h.post.name
            high_text += '%s. %s, %s, %s\r' % (index, h.fio(), post, ' '.join(org.split()))
            index += 1

        first_text = ''
        index = 1
        for f in first:
            org = f.organization
            if not org:
                org = "%s, %s" % (f.organization_name, f.territory)
            else:
                org = org.name
            if f.discipline:
                post = f.post.name + " " + f.discipline
            else:
                post = f.post.name
            first_text += '%s. %s, %s, %s\r' % (index, f.fio(), post, ' '.join(org.split()))
            index += 1

        try:
            fl = ODTFile(os.path.join(MEDIA_ROOT, 'odt/pril.odt'))
            fl.fill_template({
                "attdate": datetime.date.today().strftime("%d.%m.%Y"),
                "five": high_first_fail_text,
                "one": high_text,
                "two": first_text,
            })
            fl.save(os.path.join(MEDIA_ROOT, 'generated/pril_%s.doc' % today))
            file_link = os.path.join(MEDIA_URL, 'generated/pril_%s.doc' % today)
            return HttpResponse(file_link)
        except ODTFileError:
            return HttpResponse('GENERROR')

    return HttpResponse("GET")


def add_comment(request, rid):
    req = get_object_or_404(Request, id=rid)

    if request.method == "POST":
        comment = request.POST.get('comment', '')
        Comment.objects.create(comment=comment, request=req)

    return HttpResponseRedirect(reverse('attestation.views.request_details', args=[req.pk]))