# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.energy.forms import EnergyForm,TeploForm
from whs.energy.handlers import EnergyHandler

from piston.resource import Resource

urlpatterns = patterns('',
    url(r'^$', 'whs.energy.views.main', name='main'),
    url(ur'^Энергоресурсы/(?P<date>\d{4}-\d{2}-\d{2})/?$', 'whs.views.flat_form', {'Form':EnergyForm}, name='Energy'),
    url(ur'^Тепло/(?P<date>\d{4}-\d{2}-\d{2})/?$', 'whs.views.flat_form', {'Form':TeploForm}, name='Teplo'),
)

energy_handler = Resource(EnergyHandler)

urlpatterns += patterns('',
    url(r'^energy/$', energy_handler),
)