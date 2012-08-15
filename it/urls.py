# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url


urlpatterns = patterns('',
    url(r'^$', 'bkz.it.views.main', name='index'),
)

urlpatterns += app_urlpatterns('it')