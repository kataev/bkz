# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'whs.views.main', name='main'),
    url(r'^bills/$', 'whs.views.bills',name='bills'),
    url(r'^bills/store/$', 'whs.views.bill_store',name='bill_store'),
    url(r'^bricks/$', 'whs.views.bricks',name='bricks'),
    url(r'^bricks/store/$', 'whs.views.bricks_store',name='bricks_store'),
    url(r'^bricks/archive/$', 'whs.views.bricks_archive',name='bricks_store'),
    url(r'^agents/$', 'whs.views.agents',name='agents'),

    (r'^', include('whs.bill.urls',namespace='bill')),
    (r'^', include('whs.brick.urls',namespace='brick')),
    (r'^', include('whs.agent.urls',namespace='agent')),
    (r'^', include('whs.manufacture.urls',namespace='man')),
    (r'^', include('whs.old.urls',namespace='old')),


    (r'^dojango/', include('dojango.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^datagrid-list/(?P<app_name>.+)/(?P<model_name>.+)/$', 'dojango.views.datagrid_list', name="dojango-datagrid-list"),
)

urlpatterns += staticfiles_urlpatterns()