# -*- coding: utf-8 -*-
from bkz.utils import app_urlpatterns, patterns, url

urlpatterns = patterns('bkz.energy.views',
                       url(r'^$', 'index', name='index'),
                       url(ur'^Энергоресурсы$', 'energy', name='energy'),
                       url(ur'^Теплоэнергия$', 'teplo', name='teplo'),
) + app_urlpatterns('energy')
