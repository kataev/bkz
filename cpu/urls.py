# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('bkz.cpu.views',
                       url(r'^$', 'index', name='index'),
)


