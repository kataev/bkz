from django.conf.urls.defaults import *
from whs.manufacture.forms import *
from whs.views import UpdateView,CreateView

urlpatterns = patterns('',
    url(r'^man/$', CreateView.as_view(
        form_class=ManForm,
        model=Man
    ), name='man'),

    url(r'^man/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=ManForm,
        model=Man,
        opers=[AddFactory,]
    ), name='man-view'),

    url(r'^sort/$', CreateView.as_view(
        form_class=SortingForm,
        model=Sorting
    ), name='sort'),

    url(r'^sort/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=SortingForm,
        model=Sorting,
        opers=[SortedFactory,RemovedFactory]
    ), name='sort-view'),

    url(r'^inventory/$', CreateView.as_view(
        form_class=InventoryForm,
        model=Inventory
    ), name='inventory'),

    url(r'^inventory/(?P<pk>\d+)/$', UpdateView.as_view(
        form_class=InventoryForm,
        model=Inventory,
        opers=[Write_offFactory,]
    ), name='inventory-view'),

    )