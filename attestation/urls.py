# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from attestation.views import request_form

urlpatterns = patterns('attestation.views',
                       (r'^request/$', request_form),
                       url(r'^request/(\d+)/$', 'request_by_id'),
                       url(r'^request/(\S+)/$', 'request'),
                       url(r'^requests/$', 'requests'),
                       url(r'^completed_requests/$', 'completed_requests'),
                       url(r'^completed_requests/(\S+)/$', 'completed_requests'),
                       url(r'^details/(\d+)/$', 'request_details'),
                       url(r'^set_status/(\d+)/$', 'set_current_status'),
                       url(r'^assign/(\d+)/$', 'assign_experts'),
                       url(r'^drop_expert/(\d+)/(\d+)/$', 'drop_expert'),
                       url(r'results/(\d+)/$', 'expert_results'),
                       url(r'sheet/(\d+)/$', 'sheet'),
                       url(r'expert_sheet/(\S+)/(\d+)/$', "expert_sheet"),
                       url(r'expert_blank/(\S+)/(\d+)/$', "expert_blank"),
                       url(r'protocol/$', 'protocol'),
                       url(r'addition/$', 'addition'),
                       url(r'order/$', 'order'),
                       url(r'add_comment/(\d+)/$', 'add_comment'),
                       url(r'mark_as_completed/$', 'mark_as_completed'),

                       # ajaxed
                       url(r'^next/$', 'next_status'),
                       url(r'^save/$', 'save_grades'),
)
