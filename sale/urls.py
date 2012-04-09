# -*- coding: utf-8 -*-
from django.conf.urls import *

from whs.sale.forms import TransferFactory, SoldFactory, PalletFactory, BillForm, Bill,AgentForm
from whs.sale.views import UpdateView, CreateView, DeleteView
from whs.sale.handlers import TransferMarkHandler

from piston.resource import Resource

urlpatterns = patterns('whs.sale.views',

    url(ur'^$', 'main', name='main'),
    url(ur'^Статистика$', 'stats', name='statistics'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/удалить$', DeleteView.as_view(
        model=Bill,
    ), name='Bill-delete'),

    url(ur'^Накладная/$', CreateView.as_view(
        form_class=BillForm,
        model=Bill
    ), name='Bill'),

    url(ur'^Накладная/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, TransferFactory, PalletFactory]
    ), name='Bill-view'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, TransferFactory, PalletFactory]
    ), name='Bill-year'),

    url(ur'^Накладная/(?P<id>\d*)/печать$', 'bill_print', name='print', ),
    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/печать$', 'bill_print', name='print', ),

    url(ur'^Контрагенты$', 'agents', name='agents'),
)

urlpatterns += patterns('',
    url(ur'^Контрагент/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='Agent'),
)


transfer_mark_handler = Resource(TransferMarkHandler)

urlpatterns += patterns('',
    url(ur'^Статистика/Переводы/$', transfer_mark_handler),
)