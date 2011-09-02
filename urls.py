# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from whs.bills.forms import *

urlpatterns = patterns('',
    url(r'^$', 'whs.views.main', name='main'),

    (r'^dojango/', include('dojango.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^sentry/', include('sentry.web.urls')),

#    url(r'^1*$', 'whs.bills.views.form',{'form':transferForm},name='transasdfer'),
)
urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('whs.bills.views',
    url(r'^bill/(?P<id>\d*)/$', 'form',{'form':billForm},name='bill_get'),
    url(r'^sold/(?P<id>\d*)/$', 'form',{'form':soldForm},name='sold_get'),
    url(r'^transfer/(?P<id>\d*)/$', 'form',{'form':transferForm},name='transfer_get'),

    url(r'^bill/?(?P<id>\d*)/post/$', 'post',{'form':billForm},name='bill_post'),
    url(r'^sold/?(?P<id>\d*)/post/$', 'post',{'form':soldForm},name='sold_post'),
    url(r'^transfer/?(?P<id>\d*)/post/$', 'post',{'form':transferForm},name='transfer_post'),

    )