# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from whs.brick.forms import BrickForm

urlpatterns = patterns('',
    url(ur'^Кирпич/(?P<id>\d*)/?$', 'whs.brick.views.flat_form', {'Form':BrickForm}, name='brick'),
)