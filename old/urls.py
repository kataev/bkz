from django.conf.urls.defaults import *

urlpatterns = patterns('whs.old.views',
    url(r'^old/brick/$', 'fetch_brick',name='fetch_brick'),
    url(r'^old/opers/$', 'fetch_oper',name='fetch_oper'),
    url(r'^old/total/$', 'fetch_total',name='fetch_total'),
    )