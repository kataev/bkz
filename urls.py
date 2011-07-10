# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_restapi.model_resource import Collection
from django_restapi.responder import JSONResponder


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^fill/$', 'whs.bricks.views.fill_tree', name='fill_tree'),
#    url(r'^show_tree/$', 'whs.bricks.views.show_tree', name='show_tree'),
#    url(r'^brick/$', 'whs.bricks.views.show_brick', name='show_brick'),
#    url(r'^bill/$', 'whs.main.views.show_bill', name='show_bill'),


    url(r'^$', 'whs.main.views.main', name='main'),
    url(r'^bills/add/$', 'whs.main.views.bill_add', name='bill_add'),
    url(r'^bills/sold/add/$', 'whs.main.views.sold_add', name='sold_add'),

    url(r'^bills/sold/show/(?P<id>\d+)/$', 'whs.main.views.sold_show', name='sold_show'),
    url(r'^brick/show/(?P<id>\d+)/$', 'whs.main.views.brick_show', name='brick_show'),

    url(r'^add/(?P<model_name>\w+)/$', 'whs.main.views.ajax_add', name='ajax_add'),

    url(r'^post/(?P<modelName>\w+)/(?P<id>\d+)/$', 'whs.main.views.posting', name='posting'),

#    url(r'^test/$', 'whs.main.views.test', name='test'),
    url(r'^form/(?P<modelName>\w+)/(?P<id>\d+)/$', 'whs.main.views.form', name='form_id'),
    url(r'^form/(?P<modelName>\w+)/$', 'whs.main.views.form', name='form'),
#    url(r'^json/(?P<modelName>\w+)/(?P<id_str>.*?)/?$', 'whs.main.views.rest',name='rest'),
#    url(r'^show_tree/?$', 'whs.main.views.show_tree',name='show_tree'),
#    url(r'^rest/(.*?)/?$', bricks_model),
    (r'^dojango/', include('dojango.urls')),
#    url('^bricks/schema.(?P<extension>\w+)',  SchemaView(bricks)),
#    url('^bills/schema.(?P<extension>\w+)',  SchemaView(bills)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
)
urlpatterns += staticfiles_urlpatterns()