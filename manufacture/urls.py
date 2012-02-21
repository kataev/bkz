from django.conf.urls.defaults import *
from whs.manufacture.forms import *

urlpatterns = patterns('',
    url(r'^man/(?P<id>\d*)/?$', 'whs.views.form_get',{'form':ManForm},name='man_get'),
    url(r'^man/?(?P<id>\d*)/post/$', 'whs.views.form_post',{'form':ManForm},name='man_post'),
    )