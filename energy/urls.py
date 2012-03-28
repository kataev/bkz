# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.energy.forms import EnergyForm,TeploForm

urlpatterns = patterns('',
    url(r'^$', 'whs.energy.views.main', name='main'),
    url(ur'^Энергоресурсы/(?P<date>\d{4}-\d{2}-\d{2})/?$', 'whs.views.flat_form', {'Form':EnergyForm}, name='energy'),
    url(ur'^Тепло/(?P<date>\d{4}-\d{2}-\d{2})/?$', 'whs.views.flat_form', {'Form':TeploForm}, name='teplo'),
)
  