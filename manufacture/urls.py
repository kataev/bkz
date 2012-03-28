# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.manufacture.forms import *
from whs.views import UpdateView,CreateView

urlpatterns = patterns('',
    url(ur'^Производство/$', CreateView.as_view(
        form_class=ManForm,
        model=Man
    ), name='man'),

    url(ur'^Производство/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=ManForm,
        model=Man,
        opers=[AddFactory,]
    ), name='man-view'),

    url(ur'^Сортировка/$', CreateView.as_view(
        form_class=SortingForm,
        model=Sorting
    ), name='sort'),

    url(ur'^Сортировка/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=SortingForm,
        model=Sorting,
        opers=[SortedFactory,RemovedFactory]
    ), name='sort-view'),

    url(ur'^Инвентаризация/$', CreateView.as_view(
        form_class=InventoryForm,
        model=Inventory
    ), name='inventory'),

    url(ur'^Инвентаризация/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=InventoryForm,
        model=Inventory,
        opers=[Write_offFactory,]
    ), name='inventory-view'),

    )