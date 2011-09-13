from django.conf.urls.defaults import *
from whs.brick.forms import *

urlpatterns = patterns('whs.views',
    url(r'^brick/(?P<id>\d*)/?$', 'form_get',{'form':BrickForm},name='brick_get'),
    url(r'^brick/?(?P<id>\d*)/post/$', 'form_post',{'form':BrickForm},name='brick_post'),
    )