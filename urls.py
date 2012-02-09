# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'whs.views.main', name='main'),
    url(r'^form$', 'whs.views.form', name='form'),
    url(r'^bill/(?P<id>\d*)/?$', 'whs.views.bill', name='bill'),
    url(r'^bills?$', 'whs.views.bills', name='bills'),
)

urlpatterns += staticfiles_urlpatterns()