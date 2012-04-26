# -*- coding: utf-8 -*-
from django.conf.urls import *
from whs.man.forms import *
from whs.views import UpdateView,CreateView

urlpatterns = patterns('whs.man.views',
    url(ur'^$', 'main', name='main'),

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
        opers=[SortedFactory,RemovedFactory]
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