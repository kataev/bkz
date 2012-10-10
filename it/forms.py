# -*- coding: utf-8 -*-
import datetime
import django.forms as forms

from bkz.it.models import Device, Buy, Work, Plug
from bkz.whs.forms import DateInput

class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Device.objects.filter(type__isnull=True)

    class Meta:
        name = 'Device'
        model = Device

class BuyForm(forms.ModelForm):
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

class WorkForm(forms.ModelForm):
    class Meta:
        name = 'Work'
        model = Work
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2}),
            'status': forms.RadioSelect(),
            'date': DateInput,
            'date_finished': DateInput,
            }

    def clean(self):
        data = self.cleaned_data
        if 'status' in self.changed_data and data['status'] == 'success':
            data['date_finished'] = datetime.date.today()
        return data

class PlugForm(forms.ModelForm):
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
