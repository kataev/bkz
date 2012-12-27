# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,url,patterns

urlpatterns = patterns('bkz.whs.views',
    url(ur'^$', 'bricks', name='index'), # for deleteView
    url(ur'^$', 'bricks', name='Brick-list'),
    url(ur'^Контрагенты$', 'agents', name='Agent-list'),
    url(ur'^Реализация/$', 'bills',name='Bill-list'),
    url(ur'^Сортировка/$', 'sortings',name='Sorting-list'),

    url(ur'^Производство', 'batchs', name='Add-list'),
    url(ur'^Журнал', 'journal', name='journal'),
    url(ur'^Сверка$', 'verification', name='verification'),
    url(ur'^Переводы$', 'transfers', name='transfers'),

    url(ur'^Накладная/(?P<pk>\d+)/печать$', 'bill_print', name='Bill-print'),
) + app_urlpatterns('whs')