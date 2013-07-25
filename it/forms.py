# -*- coding: utf-8 -*-
import datetime
import django.forms as forms

from bkz.it.models import Device, Buy, Plug
from bkz.whs.forms import DateInput
from bkz.bootstrap.forms import BootstrapMixin


class DeviceForm(BootstrapMixin, forms.ModelForm):
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
            'allowed': forms.SelectMultiple(attrs={'size': 15})
        }


class BuyForm(BootstrapMixin, forms.ModelForm):
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


class PlugForm(BootstrapMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlugForm, self).__init__(*args, **kwargs)
        try:
            bill = Buy.objects.get(pk=self['bill'].value)
            self.fields['printer'].queryset = bill.cartridge.allowed.all()
            self.fields['bill'].widget.attrs['readonly'] = 'readonly'
        except Buy.DoesNotExist:
            self.fields['printer'].queryset = Device.objects.filter(type__name=u'Принтеры')

    class Meta:
        model = Plug
        name = 'Plug'
        widgets = {
            'date': DateInput,
        }
