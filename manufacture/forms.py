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

class SortingForm(forms.ModelForm):
    class Meta:
        name = 'Sorting'
        model = Sorting
#        fields = ('brick', 'amount', 'poddon', 'tara', 'info')
        verbose_name = Sorting._meta.verbose_name
        verbose_name_plural = Sorting._meta.verbose_name_plural

class SortedForm(forms.ModelForm):
    class Meta:
        name = 'Sorted'
        model = Sorted
        #        fields = ('brick', 'amount', 'poddon', 'tara', 'info')
        verbose_name = Sorted._meta.verbose_name
        verbose_name_plural = Sorted._meta.verbose_name_plural

class RemovedForm(forms.ModelForm):
    class Meta:
        name = 'Removed'
        model = Removed
        #        fields = ('brick', 'amount', 'poddon', 'tara', 'info')
        verbose_name = Removed._meta.verbose_name
        verbose_name_plural = Removed._meta.verbose_name_plural


SortedFactory = inlineformset_factory(Sorting, Sorted, extra=0, form=SortedForm, )
RemovedFactory = inlineformset_factory(Sorting, Removed, extra=0, form=RemovedForm, )