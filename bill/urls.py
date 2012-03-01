from django.conf.urls.defaults import *

urlpatterns = patterns('whs.bill.views',
    url(r'^bill/(?P<id>\d*)/?$', 'bill', name='bill'),
    url(r'^bills$', 'bills', name='bills'),

    url(r'^bill/(?P<id>\d*)/print$', 'bill_print', name='print',),
    )