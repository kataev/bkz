# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django import template
from django.forms import ModelForm, Form
from django.db.models import Model

register = template.Library()


@register.filter(name='class_name')
def class_name(value):
    if not value:
        return ''
    if isinstance(value, Model):
        return value._meta.object_name
    if isinstance(value, Form):
        return ''
    if isinstance(value, ModelForm):
        return value._meta.model.__name__
    elif issubclass(value, ModelForm):
        return value._meta.model.__name__
    elif issubclass(value, Model):
        return value.__name__
    else:
        return 'unknow'


@register.filter(name='form_name')
def form_name(value):
    return 'lab/%s_form.html' % class_name(value).lower()


@register.filter(name='model_verbose_name')
def model_verbose_name(obj):
    return obj._meta.verbose_name


@register.filter(name='model_verbose_name_initial')
def model_verbose_name_initial(obj):
    vn = obj._meta.verbose_name.split(' ')

    return


@register.filter(name='model_verbose_name_plural')
def model_verbose_name_plural(obj):
    if not obj: return ''
    if hasattr(obj._meta, 'verbose_name_plural'):
        return obj._meta.verbose_name_plural
    elif hasattr(obj._meta, 'verbose_name'):
        return obj._meta.verbose_name
    else:
        return u''


@register.filter(name='model_verbose_name_accusative')
def model_verbose_name_plural(obj):
    if not obj: return ''
    if hasattr(obj._meta, 'verbose_name_accusative'):
        return obj._meta.verbose_name_accusative
    else:
        return obj._meta.verbose_name


@register.filter(name='hash')
def hash(obj, key):
    if type(obj).__name__ == 'dict':
        return obj.get(key, '')
    else:
        return getattr(obj, key, '')


@register.filter(name='func_pluck')
def func_pluck(queryset, attr):
    attr = attr.split(' ', 1)
    if len(attr) == 2:
        func, attr = attr
    else:
        return
    if func not in ('max', 'min', 'avg', 'sum'):
        raise template.TemplateSyntaxError('Func pluck error')
    try:
        if isinstance(queryset[0], dict):
            q = [b.get(attr, 0) for b in queryset]
        else:
            q = [getattr(b, attr) for b in queryset]
        if isinstance(q[0], str):
            return
        if func == 'sum':
            return sum(q)
        elif func == 'avg':
            return round(sum(q) / len(q), 2)
        elif func == 'min':
            return min(q)
        elif func == 'max':
            return max(q)
        else:
            return
    except IndexError:
        pass
    except BaseException:
        pass


delta = {}


@register.filter(name='delta')
def delta_filter(obj, key):
    global delta
    if key == 'del':
        delta = {}
        return ''
    elif isinstance(obj, int) or isinstance(obj, float):
        val = 0
        if key in delta.keys():
            val = delta.get(key, 0.0) - obj
        delta[key] = obj
        return val


avg_dict = {}


@register.filter(name='avg')
def avg_filter(obj, key):
    global avg_dict
    if key == 'del':
        avg_dict = {}
        return ''
    if 'avg' in key or 'max' in key or 'min' in key or 'sum' in key:
        avg_dict[key] = obj
        return ''
    elif isinstance(obj, int) or isinstance(obj, float):
        return avg_dict.get('avg %s' % key, 0.0) - obj
