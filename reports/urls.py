# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'reports.views',
    url(r'^requests/by/territories/$', 'territories'),
    url(r'^requests/by/categories/$', 'categories'),
    url(r'^count/by/statuses/$', "status_counter"),
    url(r'^by/experts/$', "by_experts"),
    url(r'^first_category/$', "first_category"),
    url(r'^list/$', 'reports_list'),
)
