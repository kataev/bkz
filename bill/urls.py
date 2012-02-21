from django.conf.urls.defaults import *
from whs.bill.forms import *

urlpatterns = patterns('whs.bill.views',
    url(r'^bill/(?P<id>\d*)/?$', 'bill', name='bill'),
    url(r'^bills$', 'bills', name='bills'),
    )