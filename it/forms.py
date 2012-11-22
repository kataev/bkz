# -*- coding: utf-8 -*-
import datetime
import django.forms as forms

from bkz.it.models import Device, Buy, Plug
from bkz.whs.forms import DateInput
from bkz.bootstrap.forms import BootstrapMixin,Fieldset

class DeviceForm(BootstrapMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Device.objects.filter(type__isnull=True)
        if self.instance.type_id == 1:
            self.fields['allowed'].queryset = Device.objects.filter(type_id=2)
        elif self.instance.type_id == 2:
            self.fields['allowed'].queryset = Device.objects.filter(type_id=1)

    class Meta:
        name = 'Device'
        model = Device
        ordering = ('name',)
        widgets = {
            'allowed':forms.SelectMultiple(attrs={'size':15})
        }

class BuyForm(BootstrapMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BuyForm, self).__init__(*args, **kwargs)
        self.fields['cartridge'].queryset = Device.objects.filter(type__name=u'Картриджи')
    class Meta:
        name = 'Buy'
        model = Buy
        widgets = {
            'info': forms.Textarea(attrs={'rows': 2}),
            'date': DateInput,
        }


class PlugForm(BootstrapMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlugForm, self).__init__(*args, **kwargs)
        self.fields['bill'].queryset = Buy.objects.filter(cartridge__type__name=u'Картриджи')
        self.fields['printer'].queryset = Device.objects.filter(type__name=u'Принтеры')

    class Meta:
        model = Plug
        name = 'Plug'
    	widgets = {
            'date': DateInput,
	    }
