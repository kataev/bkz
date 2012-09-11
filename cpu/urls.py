# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.cpu.forms import DeviceForm,PositionForm

urlpatterns = patterns('',
    url(r'^$', 'bkz.cpu.views.main', name='index'),
)


