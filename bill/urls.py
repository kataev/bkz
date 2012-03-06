# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from whs.bill.forms import TransferFactory, SoldFactory, BillForm, Bill
from whs.bill.views import UpdateView, CreateView

urlpatterns = patterns('whs.bill.views',
    #    url(r'^bill/(?P<id>\d*)/?$', 'bill', name='bill'),
    url(r'^bills$', 'bills', name='bills'),
    url(ur'^Накладные$', 'bills', name='bills'),

    url(ur'^Накладная/$', CreateView.as_view(
        form_class=BillForm,
        model=Bill
    ), name='bill'),

    url(ur'^Накладная/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=BillForm,
        model=Bill,
        opers=[SoldFactory, TransferFactory]
    ), name='bill-view'),


    url(ur'^Накладная/(?P<id>\d*)/print$', 'bill_print', name='print', ),


)