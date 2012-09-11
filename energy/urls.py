# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns,patterns,url
from bkz.energy.forms import EnergyForm, TeploForm
from bkz.whs.views import DeleteView

urlpatterns = patterns('',
    url(r'^$', 'bkz.energy.views.main', name='index'),

) + app_urlpatterns('energy')