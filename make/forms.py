# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin

from bkz.make.models import Forming, Warren
from bkz.whs.forms import NumberInput,FloatInput
from bkz.lab.forms import PopUpCheckboxSelectMultiple

class FormingForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Forming
        widgets = { 'date': forms.HiddenInput(),
                    'cavitation':forms.HiddenInput(),
                    'order':forms.HiddenInput(),
                    'width':forms.HiddenInput(),
                    'color':forms.HiddenInput(),

                    'density':FloatInput(),
                    'vacuum':FloatInput,
         }
FormingFactory = modelformset_factory(Forming,form=FormingForm,extra=26,max_num=30)

class WarrenForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Warren
        exclude = ('forming','part')
        widgets = {'date':forms.HiddenInput(),
                    'tto':forms.TextInput(attrs={'tabindex':2}),
                    'tts':NumberInput(attrs={'tabindex':1}),
                    'brocken':NumberInput(attrs={}),
                    'order':forms.HiddenInput(),
                    'source':forms.HiddenInput(),
                    'cause':PopUpCheckboxSelectMultiple(attrs={'class':'checkbox'}),
                    }

WarrenFactory = modelformset_factory(Warren,form=WarrenForm,extra=26,max_num=30)

class WidthColorForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Forming
        fields = ('cavitation','width','color')
