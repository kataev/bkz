# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
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
                    'size':forms.TextInput(attrs={'tabindex':2}),
                    'poke':forms.TextInput(attrs={'tabindex':2}),
                    'stratcher':forms.TextInput(attrs={'tabindex':2}),
                    'temperature':NumberInput(attrs={'tabindex':2}),
                    'humidity':FloatInput(attrs={'tabindex':2}),
                    'sand':FloatInput(attrs={'tabindex':2}),
                    'conveyor':FloatInput(attrs={'tabindex':2}),

                    'density':FloatInput(),
                    'vacuum':FloatInput,
         }
FormingFactory = modelformset_factory(Forming,form=FormingForm,extra=26,max_num=30)

class WarrenForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Warren
        fields = ('number','date')
        widgets = {'date':forms.HiddenInput(),
                    'number':forms.TextInput(attrs={'tabindex':'2'})
                    }
        
class WarrenTTOForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Warren
        exclude = ('consumer','part','forming')
        widgets = {'date':forms.HiddenInput(),
                    'number':forms.TextInput(attrs={'tabindex':'2'}),
                    'path':NumberInput(attrs={'tabindex':'2'}),
                    'brocken':NumberInput(attrs={'tabindex':'3'}),
                    'cause':PopUpCheckboxSelectMultiple(attrs={'class':'checkbox'}),
                    }


WarrenFactory = modelformset_factory(Warren,form=WarrenForm,extra=8,max_num=10)
WarrenTTOFactory = inlineformset_factory(Warren, Warren, form=WarrenTTOForm, extra=4, max_num=5,can_delete=False)
