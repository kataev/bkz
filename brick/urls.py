from django.conf.urls.defaults import *
from whs.brick.forms import *

urlpatterns = patterns('whs.views',
    url(r'^select/$', 'brick_select',name='select'),
    url(r'^brick/(?P<id>\d*)/?$', 'form_get',{'form':BrickForm},name='brick_get'),
    url(r'^brick/?(?P<id>\d*)/post/$', 'form_post',{'form':BrickForm},name='brick_post'),
    url(r'^brick/?(?P<id>\d*)/store/$', 'brick_store',name='brick_store'),
    )