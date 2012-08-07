# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.utils import app_urlpatterns


urlpatterns = patterns('',
    url(r'^$', 'bkz.it.views.main', name='index'),
)

urlpatterns += app_urlpatterns('it')