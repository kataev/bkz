# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin,Fieldset

from bkz.make.models import Forming, Warren
from bkz.whs.forms import DateInput

class FormingForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Forming
        widgets = {'date': DateInput}

class WarrenForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Warren
        exclude = ('tts','amount')
        widgets = {'date':forms.HiddenInput}
        
class WarrenTTOForm(BootstrapMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WarrenTTOForm, self).__init__(*args,**kwargs)
        self['tt'].label = u'№ ТТО'

	class Meta:
		model = Warren

WarrenFactory = modelformset_factory(Warren,form=WarrenForm,extra=1)
WarrenTTOFactory = inlineformset_factory(Warren, Warren, WarrenTTOForm, exclude=('date',) , extra=1,can_delete=False)