from django.conf.urls.defaults import *
from whs.bill.forms import *

urlpatterns = patterns('whs.bill.views',
    url(r'^bill/(?P<id>\d*)/?$', 'bill_form_get',{'form':BillForm},name='bill_get'),
    url(r'^bill/(?P<id>\d+)/store/$', 'bill_store',{'form':BillForm},name='bill_store'),
    url(r'^bill/?(?P<id>\d*)/post/$', 'form_post',{'form':BillForm},name='bill_post'),

    url(r'^sold/(?P<id>\d*)/?$', 'opers_form_get',{'form':SoldForm},name='sold_get'),
    url(r'^sold/?(?P<id>\d*)/post/$', 'form_post',{'form':SoldForm},name='sold_post'),
    url(r'^sold/?(?P<id>\d*)/delete/$', 'delete',{'form':Confirm,'model':Sold},name='sold_delete'),

    url(r'^transfer/(?P<id>\d*)/?$', 'opers_form_get',{'form':TransferForm},name='transfer_get'),
    url(r'^transfer/?(?P<id>\d*)/post/$', 'form_post',{'form':TransferForm},name='transfer_post'),
    url(r'^transfer/?(?P<id>\d*)/delete/$', 'delete',{'form':Confirm,'model':Transfer},name='transfer_delete'),
    )