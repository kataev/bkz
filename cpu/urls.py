# -*- coding: utf-8 -*-
from django.conf.urls import patterns,url

urlpatterns = patterns('',
    url(r'^$', 'bkz.cpu.views.main', name='index'),
)


