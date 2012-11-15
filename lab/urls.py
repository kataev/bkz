# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.lab.views',
    url(ur'^$', 'index', name='index'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/печать_акта$', 'batch_print_akt', name='Batch-print_akt'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/печать_документа_о_качестве$', 'batch_print_doc', name='Batch-print_doc'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/испытания$', 'batch_tests', name='Batch-tests'),
)

urlpatterns += app_urlpatterns('lab')