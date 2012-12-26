# -*- coding: utf-8 -*-
from functools import partial

from django.conf.urls import url,patterns
from django.core.urlresolvers import reverse_lazy
from django.db.models import get_models,get_app
from django.utils.importlib import import_module
from django.views.generic import CreateView,UpdateView,DeleteView
from django.db.models import permalink

from pytils.dt import ru_strftime

def app_urlpatterns(app_name):
    urls = patterns('')
    app = get_app(app_name)
    forms = import_module('.forms',app_name)
    views = import_module('.views',app_name)
    for model in filter(lambda m:issubclass(m,UrlMixin),get_models(app)):
        name = model._meta.object_name
        if hasattr(forms,name+'Form'):
            form = getattr(forms,name+'Form',False)
        else: continue
        verbose_name = ''.join([x.capitalize() for x in model._meta.verbose_name.split(' ')])
        view = getattr(views,name+'CreateView',CreateView).as_view(form_class=form,model=model)
        u = url(ur'%s/Создать$' % verbose_name, view, name=name+'-add')
        urls.append(u)
        view = getattr(views,name+'UpdateView',UpdateView).as_view(form_class=form,model=model)
        u = url(ur'%s/(?P<pk>\d+)$' % verbose_name, view, name=name+'-change')
        urls.append(u)
        view = getattr(views,name+'DeleteView',DeleteView).as_view(model=model,success_url=reverse_lazy('%s:index'%app_name),template_name = 'core/delete.html')
        u = url(ur'%s/(?P<pk>\d+)/Удалить$' % verbose_name, view, name=name+'-delete')
        urls.append(u)
    return urls

class UrlMixin(object):
    @permalink
    def get_absolute_url(self):
        return self.get_url()

    def get_url(self):
        url = '%s:%s' % (self._meta.app_label,self._meta.object_name)
        if self.pk:
            url+='-change'
            return url, (), {'pk':self.pk}
        else:
            url+='-add'
            return url,

    @permalink
    def get_delete_url(self):
        url = '%s:%s-delete' % (self._meta.app_label,self._meta.object_name)
        return url, (), {'pk':self.pk}

ru_date = partial(ru_strftime,u'%d %B %Y',inflected=True)

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
def view_permisions(apps=None):
    if not apps: apps = ['whs', 'lab', 'energy', 'it']
    for app in apps:
        for c in ContentType.objects.filter(app_label=app):
            if issubclass(c.model_class(),UrlMixin):
                p = Permission(codename='view_%s' % c.model, name=u'Можно просматривать %s' % c.name, content_type=c)
                try:
                    p.validate_unique()
                except ValidationError:
                    pass
                else:
                    p.save()