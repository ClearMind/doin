# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'reports.views',
    url(r'^requests/by/territories/$', 'territories'),
    url(r'^requests/by/categories/$', 'categories'),
    url(r'^count/by/statuses/$', "status_counter"),
    url(r'^by/experts/$', "by_experts"),
    url(r'^first_category/(\S+)/$', "first_category"),
    url(r'^best_category/(\S+)/$', "best_category"),
    url(r'^list/$', 'reports_list'),
    url(r'^by/quarter/$', 'quarter'),
)
