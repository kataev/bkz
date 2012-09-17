# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.lab.views',
    url(ur'^$', 'index', name='index'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/печать$', 'batch_print', name='Batch-print'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/испытания$', 'batch_tests', name='Batch-tests'),
)

urlpatterns += app_urlpatterns('lab')