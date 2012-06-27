# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'whs.cpu.views.main', name='main'),
)


