# -*- coding: utf-8 -*-
from django.conf.urls import *

from bkz.whs.forms import *
from bkz.whs.views import UpdateView, CreateView, DeleteView,BillListView,BillWizard
from bkz.whs.handlers import TransferMarkHandler,TotalHandler, BrickHandler

from piston.resource import Resource

urlpatterns = patterns('bkz.whs.views',

    url(ur'^Мастер$', BillWizard.as_view([AgentForm,BillForm]), name='wizard'),

    url(ur'^Реализация$', BillListView.as_view(), name='sale'),
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

    url(ur'^$', 'brick_main', name='main'),
    url(ur'^Журнал$', 'man_main', name='man'),

    url(ur'^Производство/$', CreateView.as_view(
        form_class=ManForm,
        model=Man
    ), name='Man'),

    url(ur'^Производство/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=ManForm,
        model=Man,
        opers=[AddFactory,]
    ), name='Man-view'),

    url(ur'^Сортировка/$', CreateView.as_view(
        form_class=SortingForm,
        model=Sorting
    ), name='Sort'),

    url(ur'^Сортировка/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=SortingForm,
        model=Sorting,
        opers=[SortedFactory,]
    ), name='Sort-view'),

    url(ur'^Инвентаризация/$', CreateView.as_view(
        form_class=InventoryForm,
        model=Inventory
    ), name='Inventory'),

    url(ur'^Инвентаризация/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=InventoryForm,
        model=Inventory,
        opers=[Write_offFactory,]
    ), name='Inventory-view'),
)

urlpatterns += patterns('',
    url(ur'^Контрагент/$', 'bkz.views.flat_form', {'Form':AgentForm}, name='Agent'),
    url(ur'^Контрагент/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':AgentForm}, name='Agent-view'),
    url(ur'^Продавец/$', 'bkz.views.flat_form', {'Form':SellerForm}, name='Seller'),
    url(ur'^Продавец/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':SellerForm}, name='Seller-view'),
)


transfer_mark_handler = Resource(TransferMarkHandler)
total_handler = Resource(TotalHandler)
brick_handler = Resource(BrickHandler)

urlpatterns += patterns('',
    url(ur'^Статистика/Переводы/$', transfer_mark_handler, name='transfer_mark_handler'),
    url(ur'^Статистика/Кирпичи/$', total_handler, name='total_handler'),
)

urlpatterns += patterns('',
    url(ur'^Кирпич/$', 'bkz.whs.views.brick_flat_form', {'Form':BrickForm}, name='Brick'),
    url(ur'^Кирпич/(?P<id>\d+)/?$', 'bkz.whs.views.brick_flat_form', {'Form':BrickForm}, name='Brick-view'),
    url(r'^$', 'bkz.whs.views.brick_main', name='main'),
    url(ur'^Сверка$', 'bkz.whs.views.verification', name='verification'),
)



urlpatterns += patterns('',
    url(ur'^Кирпич/(?P<pk>\d+)/(?P<model>.+)/$', brick_handler),
)