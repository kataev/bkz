# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.it.forms import WorkForm, BuyForm, DeviceForm, PlugForm

urlpatterns = patterns('',
    url(r'^$', 'whs.it.views.main', name='main'),
    url(ur'^Устройство/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':DeviceForm}, name='Device'),
    url(ur'^Заявка/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':WorkForm}, name='Work'),
    url(ur'^Приход/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':BuyForm}, name='Buy'),
    url(ur'^Расход/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':PlugForm}, name='Plug'),
)


