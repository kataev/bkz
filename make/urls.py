# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url
from django.conf.urls import include

urlpatterns = patterns('bkz.make.views',
    url(ur'^$', 'index', name='index'),
    url(ur'^Формовка$', 'forming', name='forming'),
    url(ur'^Садка$', 'warren', name='warren'),
    url(ur'^ЦПУ/', include('bkz.cpu.urls', namespace='cpu')),
)

urlpatterns += app_urlpatterns('make')