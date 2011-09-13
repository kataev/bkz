from django.conf.urls.defaults import *
from whs.brick.forms import *

urlpatterns = patterns('whs.brick.views',
    url(r'^brick/(?P<id>\d*)/?$', 'brick_form_get',{'form':BrickForm},name='brick_get'),
    url(r'^brick/?(?P<id>\d*)/post/$', 'brick_form_post',{'form':BrickForm},name='brick_post'),
    )