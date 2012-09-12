# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('',
    url(r'^$', 'bkz.energy.views.main', name='index'),

) + app_urlpatterns('energy')