# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url

urlpatterns = patterns('bkz.lab.views',
    url(ur'^$', 'index', name='index'),
    url(ur'^Журнал/$', 'journal', name='journal'),
    url(ur'^Журнал/(?P<date>\d{4}-\d{2}-\d{2})$', 'journal', name='journal'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/печать_акта$', 'batch_print_akt', name='Batch-print_akt'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/печать_документа_о_качестве$', 'batch_print_doc', name='Batch-print_doc'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/испытания$', 'batch_tests', name='Batch-tests'),
    url(ur'^ГотоваяПродукция/(?P<pk>\d+)/испытания/печать_протокола$', 'batch_tests_print', name='Batch-tests_print'),
)

urlpatterns += app_urlpatterns('lab')