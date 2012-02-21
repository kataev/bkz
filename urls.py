# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from whs.brick.forms import BrickForm
from whs.agent.forms import AgentForm
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'whs.views.main', name='main'),
    url(r'^bill/(?P<id>\d*)/?$', 'whs.views.bill', name='bill'),
    url(r'^man/(?P<id>\d*)/?$', 'whs.views.man', name='man'),
    url(r'^brick/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':BrickForm}, name='brick'),
    url(r'^agent/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='agent'),

    url(r'^bills$', 'whs.views.bills', name='bills'),
    url(r'^agents$', 'whs.views.agents', name='agents'),
    url(r'^journal$', 'whs.views.journal', name='journal'),
    url(r'^history$', 'whs.views.history', name='history'),

    url(r'^test$', 'whs.views.test', name='test'),
)

urlpatterns += staticfiles_urlpatterns()