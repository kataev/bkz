# -*- coding: utf-8 -*-date = datetime.date.today()
__author__ = 'bteam'
import django.forms as forms
from whs.man.models import *
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
        fields = ('brick', 'amount')
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
        verbose_name = Sorted._meta.verbose_name
        verbose_name_plural = Sorted._meta.verbose_name_plural

class RemovedForm(forms.ModelForm):
    class Meta:
        name = 'Removed'
        model = Removed
        verbose_name = Removed._meta.verbose_name
        verbose_name_plural = Removed._meta.verbose_name_plural


SortedFactory = inlineformset_factory(Sorting, Sorted, extra=0, form=SortedForm, )
RemovedFactory = inlineformset_factory(Sorting, Removed, extra=0, form=RemovedForm, )


class InventoryForm(forms.ModelForm):
    class Meta:
        name = 'Inventory'
        model = Inventory
        verbose_name = Inventory._meta.verbose_name
        verbose_name_plural = Inventory._meta.verbose_name_plural

class Write_offForm(forms.ModelForm):
    class Meta:
        name = 'Write_off'
        model = Write_off
        verbose_name = Write_off._meta.verbose_name
        verbose_name_plural = Write_off._meta.verbose_name_plural


Write_offFactory = inlineformset_factory(Inventory, Write_off, extra=0, form=Write_offForm, )