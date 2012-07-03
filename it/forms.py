# -*- coding: utf-8 -*-
import datetime
import django.forms as forms
from django.db.models import Count,F,Sum

from whs.it.models import Device, Buy, Work, Plug

class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Device.objects.filter(type__isnull=True)

    class Meta:
        name = 'Device'
        model = Device

class BuyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['cartridge'].queryset = Device.objects.filter(type__name=u'Картриджи')
    class Meta:
        name = 'Buy'
        model = Buy
        widgets = {
            'info': forms.Textarea(attrs={'rows': 2}),
        }

class WorkForm(forms.ModelForm):
    class Meta:
        name = 'Work'
        model = Work
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2}),
            'status': forms.RadioSelect(),
            }

    def clean(self):
        data = self.cleaned_data
        if 'status' in self.changed_data and data['status'] == 'success':
            data['date_finished'] = datetime.date.today()
        return data

class PlugForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['cartridge'].queryset = Buy.objects.filter(cartridge__type__name=u'Картриджи')
        self.fields['printer'].queryset = Device.objects.filter(type__name=u'Принтеры')

    class Meta:
        model = Plug
        name = 'Plug'
