# -*- coding: utf-8 -*-
import datetime
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _

from attestation.models import RequestFlow, Territory, Qualification, RequestStatus
from reports.forms import DatePeriodForm


@login_required
def territories(request):
    title = _('Requests report by territories')

    done_flows = RequestFlow.objects.filter(status__is_done=True)

    territories = Territory.objects.all()
    for t in territories:
        t.count = 0
        t.ccount = 0
        t.hcount = 0
        t.fcount = 0
        t.requests = {}
        for r in t.request_set.all():
            if not r.requestflow_set.all():
                continue
            if r.requestflow_set.latest() not in done_flows:
                t.count += 1
                if not t.requests.has_key(r.qualification.name):
                    t.requests[r.qualification.name] = []
                t.requests[r.qualification.name].append(r)
                if r.qualification.for_confirmation:
                    t.ccount += 1
                elif r.qualification.first:
                    t.fcount += 1
                elif r.qualification.best:
                    t.hcount += 1

        for k in t.requests.keys():
            t.requests[k] = sorted(t.requests[k], key=attrgetter('last_name', 'first_name'))

    template = loader.get_template("reports/territories.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


@login_required
def categories(request):
    title = _('Request report by category')

    done_flows = RequestFlow.objects.filter(status__is_done=True)

    categories = Qualification.objects.all()
    for c in categories:
        c.count = 0
        c.requests = {}
        for r in c.request_set.all():
            if not r.requestflow_set.all():
                continue
            if r.requestflow_set.latest() not in done_flows:
                c.count += 1
                if r.territory:
                    terr_name = r.territory.name
                else:
                    terr_name = r.organization.territory.name
                if not c.requests.has_key(terr_name):
                    c.requests[terr_name] = []
                c.requests[terr_name].append(r)

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
            flows = RequestFlow.objects.filter(status__in=statuses).filter(
                date__lte=td + datetime.timedelta(days=1)).filter(date__gte=fd)

            experts = {}
            for f in flows:
                req = f.request
                for e in req.experts.all():
                    if not (e in experts):
                        experts[e] = 0
                    experts[e] += 1

    template = loader.get_template("reports/experts.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))