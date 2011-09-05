from django.conf.urls.defaults import *
from whs.bill.forms import *

urlpatterns = patterns('whs.bill.views',
    url(r'^bill/(?P<id>\d*)/?$', 'Bill_form',{'form':BillForm},name='bill_get'),
    url(r'^bill/?(?P<id>\d*)/post/$', 'Bill_post',{'form':BillForm},name='bill_post'),


    url(r'^sold/(?P<id>\d*)/?$', 'Operation_form_get',{'form':SoldForm},name='sold_get'),
    url(r'^sold/?(?P<id>\d*)/post/$', 'Operations_post',{'form':SoldForm},name='sold_post'),

    url(r'^transfer/(?P<id>\d*)/?$', 'Operation_form_get',{'form':TransferForm},name='transfer_get'),
    url(r'^transfer/?(?P<id>\d*)/post/$', 'Operations_post',{'form':TransferForm},name='transfer_post'),

    url(r'^finish_transfer/$', 'finish_transfer',{'form':Finish_transfer},name='finish_transfer'),
    )