from django.conf.urls.defaults import *

urlpatterns = patterns('whs.old.views',
    url(r'^old/brick/$', 'fetch_brick',name='fetch_brick'),
    url(r'^old/sold/$', 'fetch_oper',name='fetch_oper'),
    url(r'^old/tran/$', 'fetch_transfer',name='fetch_transfer'),
    url(r'^old/total/$', 'fetch_total',name='fetch_total'),
    )