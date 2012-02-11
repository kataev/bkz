# -*- coding: utf-8 -*-
__author__ = 'bteam'
import django.forms as forms
from whs.manufacture.models import *
from django.forms.models import inlineformset_factory

class ManForm(forms.ModelForm):
    class Meta:
        name = 'Man'
        model = Man
        exclude=('draft',)
#        widgets = {'date':forms.TextInput(attrs={'type':'date'}) }

class AddForm(forms.ModelForm):
    class Meta:
        name = 'Add'
        model = Add

AddFactory = inlineformset_factory(Man, Add, extra=0, form=AddForm, )