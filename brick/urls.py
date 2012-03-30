# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.brick.forms import BrickForm
from whs.brick.handlers import BrickHandler

from piston.resource import Resource

urlpatterns = patterns('',
    url(ur'^Кирпич/(?P<id>\d*)/?$', 'whs.brick.views.flat_form', {'Form':BrickForm}, name='Brick'),

    url(r'^$', 'whs.brick.views.main', name='main'),

    url(ur'^Статистика$', 'whs.views.stats', name='stats'),

    url(ur'^Помошь$', 'whs.views.help', name='help'),
)

brick_handler = Resource(BrickHandler)

urlpatterns += patterns('',
    url(r'^brick/(?P<pk>\d+)/(?P<model>.+)/(?P<year>\d{4})/(?P<month>\d+)/$', brick_handler),
)