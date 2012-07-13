# -*- coding: utf-8 -*-
from django.conf.urls import *

from bkz.lab.forms import *
#from bkz.views import UpdateView, CreateView, DeleteView

urlpatterns = patterns('',
    url(ur'^$', 'bkz.lab.views.main', name='main'),
    url(ur'^Глина/$', 'bkz.views.flat_form', {'Form':ClayForm}, name='Clay'),
    url(ur'^Глина/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':ClayForm}, name='Clay-view'),

    url(ur'^Песок/$', 'bkz.views.flat_form', {'Form':SandForm}, name='Sand'),
    url(ur'^Песок/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':SandForm}, name='Sand-view'),

    url(ur'^Глина_на_складе/$', 'bkz.views.flat_form', {'Form':StoredClayForm}, name='StoredClay'),
    url(ur'^Глина_на_складе/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':StoredClayForm}, name='StoredClay-view'),

    url(ur'^Брус/$', 'bkz.views.flat_form', {'Form':BarForm}, name='Bar'),
    url(ur'^Брус/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':BarForm}, name='Bar-view'),

    url(ur'^Сырец/$', 'bkz.views.flat_form', {'Form':RawForm}, name='Raw'),
    url(ur'^Сырец/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':RawForm}, name='Raw-view'),

    url(ur'^Водопоглащение/$', 'bkz.views.flat_form', {'Form':WaterAbsorption}, name='WaterAbsorption'),
    url(ur'^Подопоглащение/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':WaterAbsorption}, name='WaterAbsorption-view'),

    url(ur'^Высолы/$', 'bkz.views.flat_form', {'Form':Efflorescence}, name='Efflorescence'),
    url(ur'^Высолы/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':Efflorescence}, name='Efflorescence-view'),

    url(ur'^Морозостойкость/$', 'bkz.views.flat_form', {'Form':FrostResistanceForm}, name='FrostResistance'),
    url(ur'^Морозостойкость/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':FrostResistanceForm}, name='FrostResistance-view'),

    url(ur'^Плотность/$', 'bkz.views.flat_form', {'Form':DensityForm}, name='Density'),
    url(ur'^Плотность/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':DensityForm}, name='Density-view'),

    url(ur'^Партия/$', 'bkz.views.flat_form', {'Form':BarForm}, name='Batch'),
    url(ur'^Партия/(?P<id>\d*)/?$', 'bkz.views.flat_form', {'Form':BarForm}, name='Batch-view'),

)