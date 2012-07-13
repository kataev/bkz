# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.cpu.forms import DeviceForm,PositionForm

urlpatterns = patterns('',
    url(r'^$', 'whs.cpu.views.main', name='main'),
    url(ur'^Устройство/$', 'whs.views.flat_form', {'Form':DeviceForm}, name='Device'),
    url(ur'^Устройство/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':DeviceForm}, name='Device-view'),

    url(ur'^Канал/$', 'whs.views.flat_form', {'Form':PositionForm}, name='Position'),
    url(ur'^Канал/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':PositionForm}, name='Position-view'),
)


