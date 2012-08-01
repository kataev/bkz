# -*- coding: utf-8 -*-
from django.conf.urls import *

from bkz.utils import make_urls
from bkz.whs.views import BillListView,BillDeleteView
from bkz.whs.handlers import TransferMarkHandler,TotalHandler, BrickHandler

from piston.resource import Resource

urlpatterns = patterns('bkz.whs.views',
    url(ur'^Реализация$', BillListView.as_view(), name='sale'),
    url(ur'^Статистика$', 'stats', name='statistics'),
    url(ur'^Контрагенты$', 'agents', name='agents'),
    url(ur'^$', 'brick_main', name='main'),
    url(ur'^Журнал$', 'man_main', name='man'),
    url(ur'^Сверка$', 'verification', name='verification'),

    url(ur'^Накладная/(?P<pk>\d+)/удалить$', BillDeleteView.as_view(), name='Bill-delete'),
    url(ur'^Накладная/(?P<pk>\d+)/печать', 'bill_print', name='Bill-print'),
)
urlpatterns += patterns('', *make_urls('whs'))

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