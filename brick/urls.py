# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.brick.forms import BrickForm
from bkz.brick.handlers import BrickHandler

from piston.resource import Resource

urlpatterns = patterns('',
    url(ur'^Кирпич/$', 'bkz.brick.views.flat_form', {'Form':BrickForm}, name='Brick'),
    url(ur'^Кирпич/(?P<id>\d+)/?$', 'bkz.brick.views.flat_form', {'Form':BrickForm}, name='Brick-view'),
    url(r'^$', 'bkz.brick.views.main', name='main'),
    url(ur'^Сверка$', 'bkz.brick.views.verification', name='verification'),
    url(ur'^Статистика$', 'bkz.views.stats', name='stats'),
    url(ur'^Помошь$', 'bkz.views.help', name='help'),
)

brick_handler = Resource(BrickHandler)

urlpatterns += patterns('',
    url(ur'^Кирпич/(?P<pk>\d+)/(?P<model>.+)/$', brick_handler),
)