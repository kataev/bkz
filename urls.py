# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.core.urlresolvers import RegexURLResolver


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'whs.main.views.main', name='main'),


    url(r'^post/(?P<modelName>\w+)/(?P<id>\d+)/$', 'whs.main.views.posting', name='posting'),
    url(r'^bills/$', 'whs.main.views.bills', name='bills'),
    url(r'^agents/$', 'whs.main.views.agents', name='agents'),

    url(r'^form/(?P<modelName>\w+)/(?P<id>\d+)/$', 'whs.main.views.form', name='form_id'),
    url(r'^form/(?P<modelName>\w+)/$', 'whs.main.views.form', name='form'),
    
    (r'^dojango/', include('dojango.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^sentry/', include('sentry.web.urls')),
#    (r'^accounts/login/$', 'whs.main.views.login'),

)
urlpatterns += staticfiles_urlpatterns()