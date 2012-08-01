# -*- coding: utf-8 -*-
from django.conf.urls import *
from bkz.utils import make_urls


urlpatterns = patterns('',
    url(r'^$', 'bkz.it.views.main', name='main'),
)

urlpatterns += patterns('',*make_urls('it'))