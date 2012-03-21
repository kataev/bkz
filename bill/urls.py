# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from whs.bill.forms import TransferFactory, SoldFactory, PalletFactory, BillForm, Bill
from whs.bill.views import UpdateView, CreateView, DeleteView

urlpatterns = patterns('whs.bill.views',

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


)