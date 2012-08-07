# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.cpu.forms import DeviceForm,PositionForm

urlpatterns = patterns('',
    url(r'^$', 'bkz.cpu.views.main', name='index'),
    url(ur'^Устройство/$', 'bkz.views.flat_form', {'Form':DeviceForm}, name='Device'),
    url(ur'^Устройство/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':DeviceForm}, name='Device-view'),

    url(ur'^Канал/$', 'bkz.views.flat_form', {'Form':PositionForm}, name='Position'),
    url(ur'^Канал/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':PositionForm}, name='Position-view'),
)


