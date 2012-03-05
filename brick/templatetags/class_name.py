# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django import template

register = template.Library()

@register.filter(name='to_class_name')
def to_class_name(value):
    return value.__class__.__name__

@register.filter(name='model_verbose_name')
def model_verbose_name(obj):
    return obj._meta.verbose_name

@register.filter(name='model_verbose_name_plural')
def model_verbose_name_plural(obj):
    return obj._meta.verbose_name_plural
