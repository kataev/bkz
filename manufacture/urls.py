from django.conf.urls.defaults import *
from whs.manufacture.forms import *

urlpatterns = patterns('',
    url(r'^man/(?P<id>\d*)/?$', 'whs.manufacture.views.man', name='man'),
    )