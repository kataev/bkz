# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.energy.views',
    url(r'^$', 'index', name='index'),

) + app_urlpatterns('energy')