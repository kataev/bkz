# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,url,patterns
from bkz.whs.views import BillListView
from bkz.whs.handlers import TransferMarkHandler,TotalHandler, BrickHandler

from piston.resource import Resource

urlpatterns = patterns('bkz.whs.views',
    url(ur'^Реализация$', BillListView.as_view(), name='Bill-list'),
#    url(ur'^Статистика$', 'stats', name='statistics'),
    url(ur'^Контрагенты$', 'agents', name='Agent-list'),
    url(ur'^$', 'brick_main', name='Brick-list'),
    url(ur'^Производство', 'man_main', name='Add-list'),
    url(ur'^Журнал', 'journal', name='journal'),
    url(ur'^Сверка$', 'verification', name='verification'),

    url(ur'^Накладная/Мастер$', 'agent_select_or_create', name='Bill-wizard'),
    url(ur'^Накладная/(?P<pk>\d+)/печать$', 'bill_print', name='Bill-print'),
)
urlpatterns += app_urlpatterns('whs')

transfer_mark_handler = Resource(TransferMarkHandler)
total_handler = Resource(TotalHandler)
brick_handler = Resource(BrickHandler)

urlpatterns += patterns('',
    url(ur'^Статистика/Переводы/$', transfer_mark_handler, name='transfer_mark_handler'),
    url(ur'^Статистика/Кирпичи/$', total_handler, name='total_handler'),
)

urlpatterns += patterns('',
    url(ur'^Кирпич/(?P<pk>\d+)/(?P<model>.+)/$', brick_handler),
)