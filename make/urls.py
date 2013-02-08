# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.make.views',
    url(ur'^$', 'index', name='index'),
    url(ur'^Формовка$', 'forming', name='forming'),
    url(ur'^Садка$', 'warren', name='warren'),
)

urlpatterns += app_urlpatterns('make')