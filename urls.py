from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'config.views.index'),
    (r'^login/$', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}),
    url(r'^attestation/', include('attestation.urls')),
    url(r'^reports/', include('reports.urls')),

    # enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
