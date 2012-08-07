# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.energy.forms import EnergyForm, TeploForm
from bkz.energy.handlers import EnergyHandler

from piston.resource import Resource
from bkz.views import DeleteView

urlpatterns = patterns('',
    url(r'^$', 'bkz.energy.views.main', name='index'),
    url(ur'^Энергоресурсы/(?P<date>\d{4}-\d{2}-\d{2})?/?$', 'bkz.energy.views.data', {'Form': EnergyForm},
        name='Energy'),
    url(ur'^Энергоресурсы/(?P<id>\d+)?/?$', 'bkz.energy.views.data', {'Form': EnergyForm}, name='Energy-pk'),
    url(ur'^Тепло/(?P<date>\d{4}-\d{2}-\d{2})?/?$', 'bkz.energy.views.data', {'Form': TeploForm}, name='Teplo'),
    url(ur'^Тепло/(?P<id>\d+)?/?$', 'bkz.energy.views.data', {'Form': TeploForm}, name='Teplo-pk'),
    url(ur'^Энергоресурсы/(?P<pk>\d+)/удалить$', DeleteView.as_view(model=EnergyForm._meta.model,), name='Energy-delete'),
    url(ur'^Тепло/(?P<pk>\d+)/удалить$', DeleteView.as_view(model=TeploForm._meta.model,), name='Teplo-delete'),
)

energy_handler = Resource(EnergyHandler)

urlpatterns += patterns('',
    url(r'^energy/$', energy_handler),
)