# -*- coding: utf-8 -*-
from django.conf.urls import *

from whs.sale.forms import SoldFactory, PalletFactory, BillForm, Bill, AgentForm, SellerForm
from whs.sale.views import UpdateView, CreateView, DeleteView,BillListView
from whs.sale.handlers import TransferMarkHandler,TotalHandler

from piston.resource import Resource

urlpatterns = patterns('whs.sale.views',

    url(ur'^$', BillListView.as_view(), name='main'),
    url(ur'^Статистика$', 'stats', name='statistics'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/удалить$', DeleteView.as_view(
        model=Bill,
    ), name='Bill-delete'),

    url(ur'^Накладная/$', CreateView.as_view(
        form_class=BillForm,
        model=Bill
    ), name='Bill'),

    url(ur'^Накладная/(?P<pk>\d+)/$', 'bill_pk_redirect', name='Bill-view-pk'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, PalletFactory]
    ), name='Bill-year'),

    url(ur'^Накладная/(?P<id>\d*)/печать$', 'bill_print', name='print'),
    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/печать$', 'bill_print', name='print'),

    url(ur'^Контрагенты$', 'agents', name='agents'),
)

urlpatterns += patterns('',
    url(ur'^Контрагент/$', 'whs.views.flat_form', {'Form':AgentForm}, name='Agent'),
    url(ur'^Контрагент/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='Agent-view'),
    url(ur'^Продавец/$', 'whs.views.flat_form', {'Form':SellerForm}, name='Seller'),
    url(ur'^Продавец/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':SellerForm}, name='Seller-view'),
)


transfer_mark_handler = Resource(TransferMarkHandler)
total_handler = Resource(TotalHandler)

urlpatterns += patterns('',
    url(ur'^Статистика/Переводы/$', transfer_mark_handler, name='transfer_mark_handler'),
    url(ur'^Статистика/Кирпичи/$', total_handler, name='total_handler'),
)