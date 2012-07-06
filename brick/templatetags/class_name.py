# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django import template
from django.forms import ModelForm
from django.db.models import Model

register = template.Library()


@register.filter(name='class_name')
def class_name(value):
    if isinstance(value,Model):
        return value._meta.object_name
    if isinstance(value,ModelForm):
        return value._meta.model.__name__
    elif issubclass(value,ModelForm):
        return value._meta.model.__name__
    elif issubclass(value,Model):
        return value.__name__
    else:
        return 'unknow'

@register.filter(name='model_verbose_name')
def model_verbose_name(obj):
    return obj._meta.verbose_name

@register.filter(name='model_verbose_name_plural')
def model_verbose_name_plural(obj):
    if hasattr(obj._meta,'verbose_name_plural'):
        return obj._meta.verbose_name_plural
    else:
        return obj._meta.verbose_name_plural

@register.filter(name='model_verbose_name_accusative')
def model_verbose_name_plural(obj):
    if hasattr(obj._meta,'verbose_name_accusative'):
        return obj._meta.verbose_name_accusative
    else:
        return obj._meta.verbose_name


@register.filter(name='hash')
def hash(obj,key):
    if type(obj).__name__ == 'dict':
        return obj.get(key,'')
    else:
        return getattr(obj,key,'')

@register.filter(name='sum_pluck')
def sum_pluck(queryset,attr):
    try:
        if isinstance(queryset[0],dict):
            return sum([b.get(attr,0) for b in queryset])
        else:
            return sum([getattr(b,attr) for b in queryset])
    except :
        pass
