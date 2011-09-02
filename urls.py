# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'whs.views.main', name='main'),

    (r'^dojango/', include('dojango.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^sentry/', include('sentry.web.urls')),

    (r'^', include('whs.bill.urls')),
)
urlpatterns += staticfiles_urlpatterns()