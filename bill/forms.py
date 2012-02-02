# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory
from whs.bill.models import *

class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.legend = self.Meta.model._meta.verbose_name
        self.auto_id = 'doc_%s'

    class Meta:
        model = Bill
        fields = ('date', 'number', 'agent', 'proxy', 'info')

    class Media:
        pass

class SoldForm(forms.ModelForm):
    class Meta:
        model = Sold
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),}

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),}

SoldFactory = inlineformset_factory(Bill, Sold, extra=1,form=SoldForm )
TransferFactory = inlineformset_factory(Bill, Transfer, extra=1,form=TransferForm)