# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory
from whs.bill.models import *
from whs.brick.models import *
from django.core.exceptions import ValidationError

class DateForm(forms.Form):
    date = forms.DateField()


class NumberInput(forms.TextInput):
    input_type = 'number'

class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.legend = self.Meta.model._meta.verbose_name
        self.auto_id = 'doc_%s'

    class Meta:
        name = 'Bill'
        model = Bill
        fields = ('date', 'number', 'agent', 'proxy', 'info')
        widgets = {
            'number': NumberInput(attrs={'autocomplete': 'off','min':1}),
            'info':forms.Textarea(attrs={'rows':2})
        }

    class Media:
        pass


class SoldForm(forms.ModelForm):
    class Meta:
        name = 'Sold'
        model = Sold #autocomplete="off"
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),
                   'amount': NumberInput(attrs={'autocomplete': 'off','min':1}),
                   'tara': NumberInput(attrs={'autocomplete': 'off','min':0}),
                   'price': NumberInput(attrs={'autocomplete': 'off','min':1,'step':0.1}),
                   'delivery': NumberInput(attrs={'autocomplete': 'off','step':0.1}),
                   'info':forms.Textarea(attrs={'rows':2})
        }

    def clean_amount(self):
        data = self.cleaned_data
        if self.instance.pk:
            if self.instance.brick.total + self.instance.amount - data['amount'] < 0:
                raise ValidationError(dict(amount='На складе не хватет кирпича'))
        else:
            if data['brick'].total-data['amount'] < 0:
                raise ValidationError(dict(amount='На складе не хватет кирпича'))
        return data['amount']

    def clean_price(self):
        price = self.cleaned_data['price']
        print price
        return price

    def clean_transfer(self):
        data = self.cleaned_data
        if sum(map(lambda t: t.amount,data['transfer'])) > data['amount']:
            raise ValidationError(dict(transfer='Переводится больше чем отгружается'))

        return data['transfer']


class TransferForm(forms.ModelForm):
    class Meta:
        name = 'Transfer'
        model = Transfer
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),
                   'amount': NumberInput(attrs={'autocomplete': 'off','min':1}),
                   'tara': NumberInput(attrs={'autocomplete': 'off','min':0}),
                   'info':forms.Textarea(attrs={'rows':2}) }

    def clean(self):
        if self.instance.bill_sold_related.count():
            raise ValidationError('Перевод не может редактироваться когда прикреплен к продаже')
        return self.cleaned_data

SoldFactory = inlineformset_factory(Bill, Sold, extra=0, form=SoldForm, )
TransferFactory = inlineformset_factory(Bill, Transfer, extra=0, form=TransferForm, )


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
