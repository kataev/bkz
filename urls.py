# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.utils.encoding import smart_str

admin.autodiscover()

urlpatterns = patterns(u'',
    url(r'^$', 'whs.views.main', name='main'),

    url(ur'^Статистика$', 'whs.views.stats', name='stats'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('whs.brick.urls')),
    url(r'^', include('whs.agent.urls')),
    url(r'^', include('whs.bill.urls')),
    url(r'^', include('whs.manufacture.urls')),

)

urlpatterns += staticfiles_urlpatterns()