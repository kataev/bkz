# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns, patterns, url


urlpatterns = patterns('bkz.it.views',
                       url(r'^$', 'main', name='index'),
)

urlpatterns += app_urlpatterns('it')
