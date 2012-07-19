# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.db.models import get_models,get_app
from django.utils.importlib import import_module
from django.views.generic import CreateView,UpdateView

def make_urls(app_name):
    urls = []
    app = get_app(app_name)
    forms = import_module('.forms',app_name)
    views = import_module('.views',app_name)
    for model in filter(lambda m:issubclass(m,UrlMixin),get_models(app)):
        name = model._meta.object_name
        if hasattr(forms,name+'Form'):
            form = getattr(forms,name+'Form',False)
#        elif hasattr(forms,name+'FlatForm'):
#            form = getattr(forms,name+'FlatForm',False)
        else: continue
        view = getattr(views,name+'CreateView',CreateView).as_view(form_class=form,model=model)
        u = url(ur'%s/Создать' % model._meta.verbose_name.replace(' ','_'), view, name=name)
        urls.append(u)
        view = getattr(views,name+'UpdateView',UpdateView).as_view(form_class=form,model=model)
        u = url(ur'%s/(?P<pk>\d+)' % model._meta.verbose_name.replace(' ','_'), view, name=name+'-view')
        urls.append(u)
    return urls

class UrlMixin(object):
    def get_absolute_url(self):
        url = '%s:%s' % (self._meta.app_label,self._meta.object_name)
        if self.pk:url+='-view'
        return reverse(url ,kwargs=dict(pk=self.pk))