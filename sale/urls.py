# -*- coding: utf-8 -*-
from django.conf.urls import *

from whs.sale.forms import TransferFactory, SoldFactory, PalletFactory, BillForm, Bill,AgentForm
from whs.sale.views import UpdateView, CreateView, DeleteView

urlpatterns = patterns('whs.sale.views',

    url(r'^bills$', 'bills', name='bills'),
    url(ur'^Накладные$', 'bills', name='bills'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/удалить$', DeleteView.as_view(
        model=Bill,
    ), name='bill-delete'),

    url(ur'^Накладная/$', CreateView.as_view(
        form_class=BillForm,
        model=Bill
    ), name='bill'),

    url(ur'^Накладная/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, TransferFactory, PalletFactory]
    ), name='bill-view'),

    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, TransferFactory, PalletFactory]
    ), name='bill-view'),

    url(ur'^Накладная/(?P<id>\d*)/печать$', 'bill_print', name='print', ),
    url(ur'^Накладная/(?P<year>\d{4})/(?P<number>\d+)/печать$', 'bill_print', name='print', ),

    url(ur'^Контрагенты$', 'agents', name='agents'),
#    url(ur'^Контрагент/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='agent'),

)