# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(u'',
    url(r'^$', 'whs.views.index', name='index'),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(ur'^Склад/', include('whs.brick.urls', namespace='brick')),
    url(ur'^Склад/Реализация/', include('whs.sale.urls', namespace='sale')),
    url(ur'^Склад/Производство/', include('whs.man.urls', namespace='man')),
    url(ur'^Энергоресурсы/', include('whs.energy.urls', namespace='energy')),
)

urlpatterns += staticfiles_urlpatterns()