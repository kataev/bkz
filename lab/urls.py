# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.lab.views',
    url(ur'^$', 'index', name='index'),
)

urlpatterns += app_urlpatterns('lab')