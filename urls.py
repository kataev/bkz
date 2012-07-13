# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(u'',
    url(ur'^$', render, dict(template_name='index.html'), name='index'),
    url(ur'^Помошь$', render, dict(template_name='help.html'), name='help'),
    url(ur'^Прайс$', render, dict(template_name='price.html'), name='price'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(ur'^Склад/', include('bkz.whs.urls', namespace='whs')),
    url(ur'^Энергоресурсы/', include('bkz.energy.urls', namespace='energy')),
    url(ur'^Лаборатория/', include('bkz.lab.urls', namespace='lab')),
    url(ur'^ЦПУ/', include('bkz.cpu.urls', namespace='cpu')),
    url(ur'^ИТ/', include('bkz.it.urls', namespace='it')),
    url(ur'^ЦПУ/Датчики/?', include('graphite.render.urls',namespace='it')),
)

urlpatterns += staticfiles_urlpatterns()