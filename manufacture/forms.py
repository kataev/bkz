# -*- coding: utf-8 -*-
__author__ = 'bteam'
import django.forms as forms
from whs.manufacture.models import *
from django.forms.models import inlineformset_factory

class ManForm(forms.ModelForm):
    class Meta:
        name = 'Man'
        model = Man
        verbose_name = Man._meta.verbose_name
        verbose_name_plural = Man._meta.verbose_name_plural

class AddForm(forms.ModelForm):
    class Meta:
        name = 'Add'
        model = Add
        fields = ('brick', 'amount', 'poddon', 'tara', 'info')
        verbose_name = Add._meta.verbose_name
        verbose_name_plural = Add._meta.verbose_name_plural

AddFactory = inlineformset_factory(Man, Add, extra=0, form=AddForm, )