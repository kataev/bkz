# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.agent.forms import *

urlpatterns = patterns('',
    url(ur'^Контрагент/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='agent'),
    url(ur'^Контрагенты$', 'whs.agent.views.agents', name='agents'),
)