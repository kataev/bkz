# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin,Fieldset

from bkz.make.models import Forming, Warren
from bkz.whs.forms import DateInput,NumberInput,FloatInput

class FormingForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Forming
        widgets = {'date': DateInput,
                    'temperature':FloatInput,
                    'humidity':FloatInput,
                    'vacuum':FloatInput,
         }

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