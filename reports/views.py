# -*- coding: utf-8 -*-
from collections import defaultdict
import datetime
from operator import attrgetter
import os
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _

from attestation.models import RequestFlow, Territory, Qualification, RequestStatus, Request, Expert, ExpertInRequest
from libs.ODTFile import ODTFile
from reports.forms import DatePeriodForm, QuarterForm
from itertools import groupby


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
            r.request_date = r.requestflow_set.order_by('date').values_list('date', flat=True)[0]
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
        (u'Заявления на первую категорию', reverse(first_category, args=['all'])),
        (u'Заявления на первую категорию по УП', reverse(first_category, args=('simple', ))),
        (u'Заявления на высшую категорию', reverse(best_category, args=['all'])),
        (u'Заявления на высшую категорию по УП', reverse(best_category, args=('simple', ))),
        (u'Квартальный отчет', reverse(quarter)),
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
                RequestFlow.objects.filter(status__in=statuses).filter(
                    date__lte=td + datetime.timedelta(days=1),
                    date__gte=fd
                ).values_list('request_id', flat=True)
            )

            experts = {}
            data_array = ()
            start_position = (0, 1)  # A4
            number = 1

            for eir in ExpertInRequest.objects.select_related('expert', 'request'):
                if eir.request_id in flows:
                    experts.setdefault(eir.expert, []).append(eir.request)

            for expert, requests in sorted(experts.items(), key=lambda (e, _): e.__unicode__()):
                common = sorted([r.fio() for r in requests if not r.doc_for_simple])
                simple = sorted([r.fio() for r in requests if r.doc_for_simple])
                data_array += (
                    (
                        number,  # num
                        expert.__unicode__(),  # expert
                        ';\n'.join(common),  # req_common
                        ';\n'.join(simple),  # req_simple
                        len(common),  # count_common
                        len(simple),  # count_simple
                        len(common) + len(simple)  # count_overall
                    ),
                )
                number += 1

            spreadsheet = ODTFile(os.path.join(settings.MEDIA_ROOT, 'odt', 'experts.ods'))
            if data_array:
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
def first_category(request, kind):
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
                'request__post', 'request__status'
            ).filter(
                status__in=statuses,
                request__qualification__first=True,
                date__lte=td + datetime.timedelta(days=1),
                date__gte=fd
            )
            flows = filter(lambda f_: f_.request.status.is_expertise_results_received, flows)
            if kind == 'simple':
                flows = filter(
                    lambda f_: f_.request.doc_for_simple is not None and len(f_.request.doc_for_simple) > 10,
                    flows
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
                spreadsheet = ODTFile(
                    os.path.join(
                        settings.MEDIA_ROOT,
                        'odt',
                        'first_category%s.ods' % ('' if kind == 'all' else '_simple')
                    )
                )
                sheet = spreadsheet.document.getSheets().getByIndex(0)
                row = 3
                count = 1
                for territory in by_territory.keys():
                    sheet.getCellRangeByPosition(0, row, 6, row).merge(1)
                    sheet.getCellByPosition(0, row).setString(territory)
                    row += 1
                    local_flows = by_territory[territory]
                    local_flows = sorted(local_flows, key=lambda fl: (fl.request.post.name, fl.request.last_name))
                    for flow in local_flows:
                        range_ = sheet.getCellRangeByPosition(0, row, 5, row)
                        r = flow.request
                        row += 1
                        if expertises.get(r.id, None):
                            fg = sum([e.first_grade or 0 for e in expertises[r.id]])
                            sg = sum([e.second_grade or 0 for e in expertises[r.id]])
                        else:
                            fg, sg = 0, 0

                        range_.setDataArray(
                            (  # row
                                (  # columns in row
                                    count,
                                    r.fio(),
                                    r.post.name,
                                    r.organization_name or r.organization.name,
                                    fg,
                                    sg if kind == 'all' else r.doc_for_simple
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


@login_required
def best_category(request, kind):
    title = u'Отчет по заявлениям на высшую категорию'
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
                'request__post', 'request__status'
            ).filter(
                status__in=statuses,
                request__qualification__best=True,
                date__lte=td + datetime.timedelta(days=1),
                date__gte=fd
            )
            flows = filter(lambda f_: f_.request.status.is_expertise_results_received, flows)
            flows = filter(
                lambda f_: f_.request.doc_for_simple is not None and len(f_.request.doc_for_simple) > 10,
                flows
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
                spreadsheet = ODTFile(
                    os.path.join(
                        settings.MEDIA_ROOT,
                        'odt',
                        'best_category%s.ods' % ('' if kind == 'all' else '_simple')
                    )
                )
                sheet = spreadsheet.document.getSheets().getByIndex(0)
                row = 3
                count = 1
                for territory in by_territory.keys():
                    sheet.getCellRangeByPosition(0, row, 6, row).merge(1)
                    sheet.getCellByPosition(0, row).setString(territory)
                    row += 1
                    local_flows = by_territory[territory]
                    local_flows = sorted(local_flows, key=lambda fl: (fl.request.post.name, fl.request.last_name))
                    for flow in local_flows:
                        range_ = sheet.getCellRangeByPosition(0, row, 5, row)
                        r = flow.request
                        row += 1
                        if expertises.get(r.id, None):
                            fg = sum([e.first_grade or 0 for e in expertises[r.id]])
                            sg = sum([e.second_grade or 0 for e in expertises[r.id]])
                        else:
                            fg, sg = 0, 0

                        range_.setDataArray(
                            (  # row
                                (  # columns in row
                                    count,
                                    r.fio(),
                                    r.post.name,
                                    r.organization_name or r.organization.name,
                                    fg,
                                    sg if kind == 'all' else r.doc_for_simple
                                ),
                            )
                        )
                        count += 1

                file_name = os.path.join(
                    settings.MEDIA_URL,
                    'generated',
                    'best_category_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
                )
                spreadsheet.save(
                    os.path.join(
                        settings.MEDIA_ROOT,
                        'generated',
                        'best_category_%s_%s.xls' % (fd.strftime('%Y%m%d'), td.strftime('%Y%m%d'))
                    ),
                    file_format='MS Excel 97'
                )

    template = loader.get_template("reports/best_category.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))


def quarter(request):
    title = u'Квартальный отчет'
    form = QuarterForm(initial={"quarter": 'I', "year": datetime.date.today().year})

    borders = {
        'I': (datetime.datetime(2014, 1, 1, 0), datetime.datetime(2014, 4, 14, 0)),
        'II': (datetime.datetime(2014, 4, 15, 0), datetime.datetime(2014, 7, 14, 0)),
        'III': (datetime.datetime(2014, 7, 15, 0), datetime.datetime(2014, 10, 14, 0)),
        'IV': (datetime.datetime(2014, 10, 15, 0), datetime.datetime(2014, 12, 31, 0))
    }

    if request.method == 'POST':
        form = QuarterForm(request.POST)
        if form.is_valid():
            for k, v in borders.items():
                borders[k] = (
                    v[0].replace(year=form.cleaned_data['year']),
                    v[1].replace(year=form.cleaned_data['year'])
                )

            from_date, to_date = borders[form.cleaned_data['quarter']]

            requests = Request.objects.filter(
                order_date__gte=from_date,
                order_date__lte=to_date,
                organization_type__isnull=False
            ).order_by('order_number', 'order_date')

            type_filters = {
                7: lambda _: _,
                20: lambda r: r.organization_type == 'common',
                59: lambda r: r.organization_type == 'professional',
                33: lambda r: r.organization_type == 'preschool',
                46: lambda r: r.organization_type == 'additional',
                111: lambda r: r.organization_type == 'social',
                98: lambda r: r.organization_type == 'cultural',
                72: lambda r: r.organization_type == 'correction',
                85: lambda r: r.organization_type == 'sport'
            }

            spreadsheet = ODTFile(os.path.join(settings.MEDIA_ROOT, 'odt', 'quarter.ods'))
            sheet = spreadsheet.document.getSheets().getByIndex(0)

            # sub sub titles
            for r in range(5, 110, 13):
                start = (0, r+2)
                array = ()

                sheet.getCellByPosition(0, r).setString(u'Отчет за %s квартал %s года' % (
                    form.cleaned_data['quarter'],
                    form.cleaned_data['year']
                ))

                requests_ = filter(type_filters[start[1]], requests)

                if not requests_:
                    continue

                by_order = {k: list(v) for k, v in groupby(
                    requests_, key=lambda f_: (f_.order_number, f_.order_date)
                )}

                for order, reqs in sorted(by_order.items(), key=lambda o: o[0]):
                    if not all(order):
                        continue
                    array += (
                        (
                            u'Приказ Департамента № %s' % order[0],
                            order[1].strftime('%d.%m.%Y'),
                            len([1 for r in reqs if r.status.is_done and r.qualification.first]),
                            len([1 for r in reqs if r.status.is_done and r.qualification.best]),
                            len([1 for r in reqs if r.status.is_fail and r.qualification.first]),
                            len([1 for r in reqs if r.status.is_fail and r.qualification.best]),
                            len([1 for r in reqs if r.status.is_done])
                        ),
                    )

                range_ = sheet.getCellRangeByPosition(
                    start[0], start[1], start[0] + len(array[0]) - 1, start[1] + len(array) - 1
                )
                range_.setDataArray(array)

            file_name = os.path.join(
                settings.MEDIA_URL,
                'generated',
                'quarter_%s_%s.xls' % (
                    form.cleaned_data['quarter'],
                    form.cleaned_data['year']
                )
            )
            spreadsheet.save(
                os.path.join(
                    settings.MEDIA_ROOT,
                    'generated',
                    'quarter_%s_%s.xls' % (
                        form.cleaned_data['quarter'],
                        form.cleaned_data['year']
                    )
                ),
                file_format='MS Excel 97'
            )

    template = loader.get_template("reports/quarter.html")
    c = RequestContext(request, locals())
    return HttpResponse(template.render(c))