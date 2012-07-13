# -*- coding: utf-8 -*-
from django.conf.urls import *

from whs.lab.forms import *
#from whs.views import UpdateView, CreateView, DeleteView

urlpatterns = patterns('',
    url(ur'^$', 'whs.lab.views.main', name='main'),
    url(ur'^Глина/$', 'whs.views.flat_form', {'Form':ClayForm}, name='Clay'),
    url(ur'^Глина/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':ClayForm}, name='Clay-view'),

    url(ur'^Песок/$', 'whs.views.flat_form', {'Form':SandForm}, name='Sand'),
    url(ur'^Песок/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':SandForm}, name='Sand-view'),

    url(ur'^Глина_на_складе/$', 'whs.views.flat_form', {'Form':StoredClayForm}, name='StoredClay'),
    url(ur'^Глина_на_складе/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':StoredClayForm}, name='StoredClay-view'),

    url(ur'^Брус/$', 'whs.views.flat_form', {'Form':BarForm}, name='Bar'),
    url(ur'^Брус/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':BarForm}, name='Bar-view'),

    url(ur'^Сырец/$', 'whs.views.flat_form', {'Form':RawForm}, name='Raw'),
    url(ur'^Сырец/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':RawForm}, name='Raw-view'),

    url(ur'^Водопоглащение/$', 'whs.views.flat_form', {'Form':WaterAbsorption}, name='WaterAbsorption'),
    url(ur'^Подопоглащение/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':WaterAbsorption}, name='WaterAbsorption-view'),

    url(ur'^Высолы/$', 'whs.views.flat_form', {'Form':Efflorescence}, name='Efflorescence'),
    url(ur'^Высолы/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':Efflorescence}, name='Efflorescence-view'),

    url(ur'^Морозостойкость/$', 'whs.views.flat_form', {'Form':FrostResistanceForm}, name='FrostResistance'),
    url(ur'^Морозостойкость/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':FrostResistanceForm}, name='FrostResistance-view'),

    url(ur'^Плотность/$', 'whs.views.flat_form', {'Form':DensityForm}, name='Density'),
    url(ur'^Плотность/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':DensityForm}, name='Density-view'),

    url(ur'^Партия/$', 'whs.views.flat_form', {'Form':BarForm}, name='Batch'),
    url(ur'^Партия/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':BarForm}, name='Batch-view'),

)