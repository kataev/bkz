# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(u'',
    url(ur'^$', render, dict(template_name='core/index.html'), name='index'),
    url(ur'^Помошь$', render, dict(template_name='core/help.html'), name='help'),
    url(ur'^Прайс$', render, dict(template_name='core/price.html'), name='price'),
    url(ur'^Доклад$', render, dict(template_name='core/presentation.html'), name='presentation'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),

    url(ur'^Склад/', include('bkz.whs.urls', namespace='whs')),
    url(ur'^Показания/', include('bkz.energy.urls', namespace='energy')),
    url(ur'^Лаборатория/', include('bkz.lab.urls', namespace='lab')),
    url(ur'^Производство/', include('bkz.make.urls', namespace='make')),
    url(ur'^ИТ/', include('bkz.it.urls', namespace='it'), name='it'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(ur'^Вход$', 'login', {'template_name': 'core/login.html'}, name='login'),
    url(ur'^Выход$', 'logout_then_login', name='logout'),
)

urlpatterns += staticfiles_urlpatterns()
