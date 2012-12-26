# -*- coding: utf-8 -*-
import datetime

from bkz.utils import app_urlpatterns,url,patterns
from bkz.whs.views import BillListView

urlpatterns = patterns('bkz.whs.views',
    url(ur'^$', 'brick_main', name='Brick-list'),
    url(ur'^Контрагенты$', 'agents', name='Agent-list'),
    url(ur'^Реализация/$', 'bills',name='Bill-list'),

    url(ur'^Производство', 'man_main', name='Add-list'),
    url(ur'^Журнал', 'journal', name='journal'),
    url(ur'^Сверка$', 'verification', name='verification'),
    
    url(ur'^Накладная/(?P<pk>\d+)/печать$', 'bill_print', name='Bill-print'),
) + app_urlpatterns('whs')