# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(u'',
    url(r'^$', 'bkz.views.index', name='index'),
    url(ur'^Прайс$', 'bkz.views.price', name='price'),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(ur'^Склад/', include('bkz.brick.urls', namespace='brick')),
    url(ur'^Склад/Реализация/', include('bkz.whs.urls', namespace='whs')),
    url(ur'^Энергоресурсы/', include('bkz.energy.urls', namespace='energy')),
    url(ur'^Лаборатория/', include('bkz.lab.urls', namespace='lab')),
    url(ur'^ЦПУ/', include('bkz.cpu.urls', namespace='cpu')),
    url(ur'^ИТ/', include('bkz.it.urls', namespace='it')),
    url(ur'^ЦПУ/Датчики/?', include('graphite.render.urls',namespace='it')),
)

urlpatterns += staticfiles_urlpatterns()