from django.conf.urls.defaults import *
from whs.manufacture.forms import *

urlpatterns = patterns('whs.views',
    url(r'^man/(?P<id>\d*)/?$', 'form_get',{'form':ManForm},name='man_get'),
    url(r'^man/?(?P<id>\d*)/post/$', 'form_post',{'form':ManForm},name='man_post'),
    )