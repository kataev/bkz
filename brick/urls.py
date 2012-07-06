# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.brick.forms import BrickForm
from whs.brick.handlers import BrickHandler

from piston.resource import Resource

urlpatterns = patterns('',
    url(ur'^Кирпич/$', 'whs.brick.views.flat_form', {'Form':BrickForm}, name='Brick'),
    url(ur'^Кирпич/(?P<id>\d+)/?$', 'whs.brick.views.flat_form', {'Form':BrickForm}, name='Brick-view'),
    url(r'^$', 'whs.brick.views.main', name='main'),
    url(ur'^Сверка$', 'whs.brick.views.verification', name='verification'),
    url(ur'^Статистика$', 'whs.views.stats', name='stats'),
    url(ur'^Помошь$', 'whs.views.help', name='help'),
)

brick_handler = Resource(BrickHandler)

urlpatterns += patterns('',
    url(ur'^Кирпич/(?P<pk>\d+)/(?P<model>.+)/$', brick_handler),
)