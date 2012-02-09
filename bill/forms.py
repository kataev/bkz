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
        name = 'Bill'
        model = Bill
        fields = ('date', 'agent', 'proxy','number', 'info')

    class Media:
        pass

class SoldForm(forms.ModelForm):
    class Meta:
        name = 'Sold'
        model = Sold #autocomplete="off"
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),}

class TransferForm(forms.ModelForm):
    class Meta:
        name = 'Transfer'
        model = Transfer
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),}

SoldFactory = inlineformset_factory(Bill, Sold, extra=1,form=SoldForm,)
TransferFactory = inlineformset_factory(Bill, Transfer, extra=1,form=TransferForm,)


class BillFilter(forms.Form):
    date__lte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Конец периода'}))
    date__gte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Начало периода'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        """
        Изменение пустой ичейки для подсказки.
        """
        super(BillFilter, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'