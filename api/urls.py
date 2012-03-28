# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django.conf.urls import *
from piston.resource import Resource
from handlers import BrickHandler

brick_handler = Resource(BrickHandler)

urlpatterns = patterns('',
    url(r'^brick/(?P<pk>\d+)/(?P<model>.+)/(?P<year>\d{4})/(?P<month>\d+)/$', brick_handler),
)
