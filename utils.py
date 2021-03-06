# -*- coding: utf-8 -*-
from functools import partial

from django.contrib import messages
from django.conf.urls import url, patterns
from django.core.urlresolvers import reverse_lazy
from django.db.models import get_models, get_app
from django.utils.importlib import import_module
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.db.models import permalink
from pytils.dt import ru_strftime
from bkz.log import construct_change_message, log_addition, log_change, log_deletion


def get_form(self, form_class):
    form = form_class(**self.get_form_kwargs())
    for key in self.request.GET:
        try:
            form.fields[key].initial = self.request.GET[key]
        except KeyError:
            pass
    return form


def form_valid(self, form):
    self.object = form.save()
    if isinstance(self, CreateView):
        log_addition(self.request, self.object)
    else:
        message = construct_change_message(form, [])
        log_change(self.request, self.object, message)
    messages.success(self.request, u'Сохранено')
    return super(ModelFormMixin, self).form_valid(form)


def form_invalid(self, form):
    messages.error(self.request, u'Найденны ошибки')
    return self.render_to_response(self.get_context_data(form=form))


def post(self, *args, **kwargs):
    self.object = self.get_object()
    log_deletion(self.request, self.object, unicode(self.object))
    return self.delete(*args, **kwargs)


CreateView.get_form = get_form
CreateView.form_valid = form_valid
CreateView.form_invalid = form_invalid
UpdateView.form_valid = form_valid
UpdateView.form_invalid = form_invalid
DeleteView.post = post


def app_urlpatterns(app_name):
    urls = patterns('')
    app = get_app(app_name)
    forms = import_module('.forms', app_name)
    views = import_module('.views', app_name)
    for model in filter(lambda m: issubclass(m, UrlMixin), get_models(app)):
        name = model._meta.object_name
        try:
            form = getattr(forms, name + 'Form')
        except AttributeError:
            raise ImportError(app_name + '.' + name)
        verbose_name = ''.join([x.capitalize() for x in model._meta.verbose_name.split(' ')])
        view = getattr(views, name + 'CreateView', CreateView).as_view(form_class=form, model=model)
        u = url(ur'%s/Создать$' % verbose_name, view, name=name + '-add')
        urls.append(u)
        view = getattr(views, name + 'UpdateView', UpdateView).as_view(form_class=form, model=model)
        u = url(ur'%s/(?P<pk>\d+)$' % verbose_name, view, name=name + '-change')
        urls.append(u)
        view = getattr(views, name + 'DeleteView', DeleteView).as_view(model=model,
                                                                       success_url=reverse_lazy('%s:index' % app_name),
                                                                       template_name='core/delete.html')
        u = url(ur'%s/(?P<pk>\d+)/Удалить$' % verbose_name, view, name=name + '-delete')
        urls.append(u)
    return urls


class UrlMixin(object):
    @permalink
    def get_absolute_url(self):
        return self.get_url()

    def get_url(self):
        url = '%s:%s' % (self._meta.app_label, self._meta.object_name)
        if self.pk:
            url += '-change'
            return url, (), {'pk': self.pk}
        else:
            url += '-add'
            return url,

    @permalink
    def get_delete_url(self):
        url = '%s:%s-delete' % (self._meta.app_label, self._meta.object_name)
        return url, (), {'pk': self.pk}


ru_date = partial(ru_strftime, u'%d %B %Y', inflected=True)

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError


def view_permisions(apps=None):
    if not apps: apps = ['whs', 'lab', 'energy', 'it']
    for app in apps:
        for c in ContentType.objects.filter(app_label=app):
            if issubclass(c.model_class(), UrlMixin):
                p = Permission(codename='view_%s' % c.model, name=u'Можно просматривать %s' % c.name, content_type=c)
                try:
                    p.validate_unique()
                except ValidationError:
                    pass
                else:
                    p.save()
