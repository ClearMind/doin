# -*- coding: utf-8 -*-
from collections import defaultdict
import datetime
from operator import attrgetter
import os
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _

from attestation.models import RequestFlow, Territory, Qualification, RequestStatus, Request, Expert, ExpertInRequest
from libs.ODTFile import ODTFile
from reports.forms import DatePeriodForm


@login_required
def territories(request):
    title = _('Requests report by territories')

    requests = Request.objects.select_related(
        'status', 'qualification', 'territory', 'organization__territory', 'organization', 'with_qualification', 'post'
    ).filter(status__is_done=False, status__is_rejected=False, status__is_fail=False)

    by_territory = {}
    for r in requests:
        by_territory.setdefault(r.territory, []).append(r)

    territories_ = Territory.objects.all()
    for t in territories_:
        t.count = 0
        t.hcount = 0
        t.fcount = 0
        t.requests = {}
        for r in by_territory.get(t, []):
            if r.qualification.first:
                t.fcount += 1
            elif r.qualification.best:
                t.hcount += 1
            elif r.qualification.for_confirmation:
                continue
            t.count += 1
            t.requests.setdefault(r.qualification.name, []).append(r)

        for k in t.requests.keys():
            t.requests[k] = sorted(t.requests[k], key=attrgetter('last_name', 'first_name'))

    template = loader.get_template("reports/territories.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def categories(request):
    title = _('Request report by category')

    requests = Request.objects.select_related(
        'status', 'qualification', 'territory', 'organization__territory', 'organization', 'with_qualification', 'post'
    ).filter(status__is_done=False, status__is_rejected=False, status__is_fail=False)
    categories_ = Qualification.objects.exclude(for_confirmation=True)

    by_category = {}
    for r in requests:
        by_category.setdefault(r.qualification, []).append(r)

    for c in categories_:
        c.count = 0
        c.requests = {}
        for r in by_category.get(c, []):
            c.count += 1
            if r.territory:
                terr_name = r.territory.name
            else:
                terr_name = r.organization.territory.name
            c.requests.setdefault(terr_name, []).append(r)

        for k in c.requests.keys():
            c.requests[k] = sorted(c.requests[k], key=attrgetter('last_name', 'first_name'))

    template = loader.get_template("reports/categories.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def status_counter(request):
    title = _('Report by statuses in date range')
    custom_styles = ['smoothness/jquery-ui-1.8.23.custom.css', 'jquery.dataTables.css']
    custom_scripts = ['libs/jquery.dataTables.min.js']

    statuses = RequestStatus.objects.all()
    form = DatePeriodForm(initial={"fromdate": datetime.date.today(), "todate": datetime.date.today()})

    if request.method == "POST":
        form = DatePeriodForm(request.POST)
        if form.is_valid():
            todate = form.cleaned_data['todate']
            fromdate = form.cleaned_data['fromdate']
            flows = RequestFlow.objects.select_related("status").filter(
                date__lte=todate + datetime.timedelta(days=1)).filter(date__gte=fromdate)

            st = request.POST.get('status', "-1")
            if st > 0:
                try:
                    status = RequestStatus.objects.get(id=st)
                    flows = flows.filter(status=status)
                except ObjectDoesNotExist:
                    pass

            counter = {}
            for f in flows:
                status_name = f.status.name
                if not status_name in counter.keys():
                    counter[status_name] = 0
                counter[status_name] += 1

    template = loader.get_template("reports/status_counter.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def reports_list(request):
    title = _('Reports')

    list_ = [
        (_('By territories'), reverse(territories)),
        (_('By requested categories'), reverse(categories)),
        (_('By statuses'), reverse(status_counter)),
        (_('By experts'), reverse(by_experts)),
        (u'Заявления на первую категорию', reverse(first_category)),
    ]

    template = loader.get_template("reports/reports_list.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def by_experts(request):
    title = _('Report by experts')
    custom_styles = ['smoothness/jquery-ui-1.8.23.custom.css', 'jquery.dataTables.css']
    custom_scripts = ['libs/jquery.dataTables.min.js']

    form = DatePeriodForm(initial={"fromdate": datetime.date.today(), "todate": datetime.date.today()})

    if request.method == "POST":
        form = DatePeriodForm(request.POST)
        if form.is_valid():
            fd = form.cleaned_data['fromdate']
            td = form.cleaned_data['todate']

            statuses = RequestStatus.objects.filter(is_expertise_results_received=True)
            flows = set(
                f.request_id for f in
                RequestFlow.objects.filter(status__in=statuses).filter(
                    date__lte=td + datetime.timedelta(days=1),
                    date__gte=fd
                )
            )

            experts = {}
            data_array = ()
            start_position = (0, 3)  # A4
            number = 1
            counts = defaultdict(lambda: defaultdict(int))

            for eir in ExpertInRequest.objects.select_related(
                'expert', 'request', 'request__qualification'
            ).order_by('expert__last_name', 'request__last_name'):
                expert_ = eir.expert
                if eir.request_id in flows:
                    request_ = eir.request
                    if eir.first_grade and eir.second_grade:
                        request_.count_ = 3
                        if request_.qualification.best:
                            counts[expert_]['first_best_count_'] += 1
                            counts[expert_]['second_best_count_'] += 1
                        if request_.qualification.first:
                            counts[expert_]['first_first_count_'] += 1
                            counts[expert_]['second_first_count_'] += 1
                    elif eir.first_grade:
                        request_.count_ = 1
                        if request_.qualification.best:
                            counts[expert_]['first_best_count_'] += 1
                        if request_.qualification.first:
                            counts[expert_]['first_first_count_'] += 1
                    elif eir.second_grade:
                        request_.count_ = 2
                        if request_.qualification.best:
                            counts[expert_]['second_best_count_'] += 1
                        if request_.qualification.first:
                            counts[expert_]['second_first_count_'] += 1
                    else:
                        request_.count_ = None
                    experts.setdefault(eir.expert, []).append(request_)

            for expert, requests in experts.items():
                data_array += (
                    (
                        number,
                        expert.__unicode__(),
                        ';\n'.join((r.fio() for r in requests if r.qualification.best and r.count_ and r.count_ % 2)),
                        ';\n'.join((r.fio() for r in requests if r.qualification.best and r.count_ and r.count_ >= 2)),
                        ';\n'.join((r.fio() for r in requests if r.qualification.first and r.count_ and r.count_ % 2)),
                        ';\n'.join((r.fio() for r in requests if r.qualification.first and r.count_ and r.count_ >= 2)),
                        counts[expert]['first_best_count_'],
                        counts[expert]['second_best_count_'],
                        counts[expert]['first_first_count_'],
                        counts[expert]['second_first_count_']
                    ),
                )
                number += 1

            spreadsheet = ODTFile(os.path.join(settings.MEDIA_ROOT, 'odt', 'experts.ods'))
            spreadsheet.fill_spreadsheet(start_position, data_array)

            file_name = os.path.join(
                settings.MEDIA_URL,
                'generated',
                'experts_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
            )
            spreadsheet.save(
                os.path.join(
                    settings.MEDIA_ROOT,
                    'generated',
                    'experts_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
                ),
                file_format='MS Excel 97'
            )

    template = loader.get_template("reports/experts.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def first_category(request):
    title = u'Отчет по заявлениям на первую категорию'
    form = DatePeriodForm(initial={"fromdate": datetime.date.today(), "todate": datetime.date.today()})
    custom_styles = ['smoothness/jquery-ui-1.8.23.custom.css']

    if request.method == "POST":
        form = DatePeriodForm(request.POST)
        if form.is_valid():
            fd = form.cleaned_data['fromdate']
            td = form.cleaned_data['todate']

            statuses = RequestStatus.objects.filter(is_expertise_results_received=True)
            flows = RequestFlow.objects.select_related(
                'request', 'request__territory', 'request__organization', 'request__organization__territory',
                'request__post'
            ).filter(
                status__in=statuses,
                request__qualification__first=True,
                date__lte=td + datetime.timedelta(days=1),
                date__gte=fd
            )

            by_territory = {}
            for f in flows:
                if f.request.territory:
                    by_territory.setdefault(f.request.territory.name, []).append(f)
                elif f.request.organization.territory:
                    by_territory.setdefault(f.request.organization.territory.name, []).append(f)

            expertises = {}
            for e in ExpertInRequest.objects.all():
                expertises.setdefault(e.request_id, []).append(e)

            if flows:
                spreadsheet = ODTFile(os.path.join(settings.MEDIA_ROOT, 'odt', 'first_category.ods'))
                sheet = spreadsheet.document.getSheets().getByIndex(0)
                row = 3
                count = 1
                for territory in by_territory.keys():
                    sheet.getCellRangeByPosition(0, row, 7, row).merge(1)
                    sheet.getCellByPosition(0, row).setString(territory)
                    row += 1
                    local_flows = by_territory[territory]
                    local_flows = sorted(local_flows, key=lambda fl: fl.request.post.name)
                    for flow in local_flows:
                        range_ = sheet.getCellRangeByPosition(0, row, 6, row)
                        r = flow.request
                        row += 1
                        fg = sum([e.first_grade or 0 for e in expertises[r.id]])
                        sg = sum([e.second_grade or 0 for e in expertises[r.id]])
                        range_.setDataArray(
                            (  # row
                                (  # columns in row
                                    count,
                                    r.post.name,
                                    r.fio(),
                                    r.organization_name or r.organization.name,
                                    fg,
                                    sg,
                                    fg + sg
                                ),
                            )
                        )
                        count += 1

                file_name = os.path.join(
                    settings.MEDIA_URL,
                    'generated',
                    'first_category_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
                )
                spreadsheet.save(
                    os.path.join(
                        settings.MEDIA_ROOT,
                        'generated',
                        'first_category_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
                    ),
                    file_format='MS Excel 97'
                )

    template = loader.get_template("reports/first_category.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))