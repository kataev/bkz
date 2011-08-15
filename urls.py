# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from whs.bills.forms import *

urlpatterns = patterns('',
    url(r'^$', 'whs.main.views.main', name='main'),
    url(r'^brick/(\d+)/$', 'whs.bricks.views.form',name='brick'),

    (r'^dojango/', include('dojango.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^sentry/', include('sentry.web.urls')),
)
urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('whs.bills.views',
    url(r'^bill/new/$', 'form',{'form':billForm},name='bill_new'),
    url(r'^sold/new/$', 'form',{'form':soldForm},name='sold_new'),
    url(r'^transfer/new/$', 'form',{'form':transferForm},name='transfer_new'),

    url(r'^bill/(?P<id>\d+)/$', 'form',{'form':billForm},name='bill'),
    url(r'^sold/(?P<id>\d+)/$', 'form',{'form':soldForm},name='sold'),
    url(r'^transfer/(?P<id>\d+)/$', 'form',{'form':transferForm},name='transfer'),
    )