from django.conf.urls.defaults import *
from whs.manufacture.forms import *

urlpatterns = patterns('whs.manufacture.views',
    url(r'^man/(?P<id>\d*)/?$', 'man', name='man'),
    url(r'^sort/(?P<id>\d*)/?$', 'srt', name='srt'),
    )