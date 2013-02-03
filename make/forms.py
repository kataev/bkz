# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin

from bkz.make.models import Forming, Warren
from bkz.whs.forms import DateInput,NumberInput,FloatInput

class FormingForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Forming
        widgets = { 'date': forms.HiddenInput(),
                    'cavitation':forms.HiddenInput(),
                    'width':forms.HiddenInput(),
                    'color':forms.HiddenInput(),
                    'size':forms.TextInput(attrs={'tabindex':-1}),
                    'poke':forms.TextInput(attrs={'tabindex':-1}),
                    'stratcher':forms.TextInput(attrs={'tabindex':-1}),
                    'temperature':NumberInput(attrs={'tabindex':-1}),
                    'humidity':FloatInput(attrs={'tabindex':-1}),
                    'sand':FloatInput(attrs={'tabindex':-1}),
                    'k':FloatInput(attrs={'tabindex':-1}),

                    'density':FloatInput(),
                    'vacuum':FloatInput,
         }
FormingFactory = modelformset_factory(Forming,form=FormingForm,extra=26,max_num=30)         

class WarrenForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Warren
        exclude = ('consumer','amount')
        widgets = {'date':forms.HiddenInput(),
                    'source':forms.HiddenInput(),
                    'number':NumberInput(attrs={'placeholder':u'№ ТТО'})
                    }
        
class WarrenTTOForm(BootstrapMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WarrenTTOForm, self).__init__(*args,**kwargs)
        self['number'].label = u'№ ТТО'

	class Meta:
		model = Warren
        # widgets = {'number':forms.TextInput(attrs={'placeholder':u'№ ТТC'})}

WarrenFactory = modelformset_factory(Warren,form=WarrenForm,extra=6,max_num=6)
WarrenTTOFactory = inlineformset_factory(Warren, Warren, WarrenTTOForm, exclude=('date',) , extra=6, max_num=6,can_delete=False)