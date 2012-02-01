from django.conf.urls.defaults import *
from piston.resource import Resource
from handlers import *

brick_resource = Resource(BrickHandler)
brick_table_resource = Resource(BrickTableHandler)

urlpatterns = patterns('',
    url(r'^brick/(?P<id>\d+)$', brick_resource),
    url(r'^brick', brick_resource),

    url(r'^table/(?P<id>\d+)$', brick_table_resource),
    url(r'^table', brick_table_resource),



)