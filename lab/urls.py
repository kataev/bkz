# -*- coding: utf-8 -*-
from django.conf.urls import *

from bkz.lab.forms import *
from bkz.utils import app_urlpatterns
from django.shortcuts import render
#from bkz.views import UpdateView, CreateView, DeleteView
from bkz.lab.views import BatchCreateView,BatchUpdateView,BatchListView
from bkz.lab.forms import PartFactory,FlexionFactory,PressureFactory


urlpatterns = patterns('',
    url(ur'^$', BatchListView.as_view(), name='index'),
)

urlpatterns += app_urlpatterns('lab')