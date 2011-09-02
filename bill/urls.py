from django.conf.urls.defaults import *
from whs.bill.forms import *

urlpatterns = patterns('whs.bill.views',
    url(r'^bill/(?P<id>\d*)/?$', 'form',{'form':BillForm},name='bill_get'),
    url(r'^sold/(?P<id>\d*)/?$', 'form',{'form':SoldForm},name='sold_get'),
    url(r'^transfer/(?P<id>\d*)/?$', 'form',{'form':TransferForm},name='transfer_get'),

    url(r'^bill/?(?P<id>\d*)/post/$', 'post',{'form':BillForm},name='bill_post'),
    url(r'^sold/?(?P<id>\d*)/post/$', 'post',{'form':SoldForm},name='sold_post'),
    url(r'^transfer/?(?P<id>\d*)/post/$', 'post',{'form':TransferForm},name='transfer_post'),

    )