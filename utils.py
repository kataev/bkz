# -*- coding: utf-8 -*-
from django.conf.urls import url,patterns
from django.core.urlresolvers import reverse_lazy
from django.db.models import get_models,get_app
from django.utils.importlib import import_module
from django.views.generic import CreateView,UpdateView,DeleteView
from django.db.models import permalink

import pytils

def app_urlpatterns(app_name):
    urls = patterns('')
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
        u = url(ur'%s/Создать$' % model._meta.verbose_name.replace(' ','_'), view, name=name+'-add')
        urls.append(u)
        view = getattr(views,name+'UpdateView',UpdateView).as_view(form_class=form,model=model)
        u = url(ur'%s/(?P<pk>\d+)$' % model._meta.verbose_name.replace(' ','_'), view, name=name+'-change')
        urls.append(u)
        view = getattr(views,name+'DeleteView',DeleteView).as_view(model=model,success_url=reverse_lazy('%s:index'%app_name),template_name = 'core/delete.html')
        u = url(ur'%s/(?P<pk>\d+)/Удалить$' % model._meta.verbose_name.replace(' ','_'), view, name=name+'-delete')
        urls.append(u)
    return urls

class UrlMixin(object):
    @permalink
    def get_absolute_url(self):
        url = '%s:%s' % (self._meta.app_label,self._meta.object_name)
        if self.pk:url+='-change'
        else:url+='-add'
        return (url, (), {'pk':self.pk})

    @permalink
    def get_delete_url(self):
        url = '%s:%s-delete' % (self._meta.app_label,self._meta.object_name)
        return (url, (), {'pk':self.pk})

def ru_date(date):
    return pytils.dt.ru_strftime(u'%d %B %Y',inflected=True,date=date)