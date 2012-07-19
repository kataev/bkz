# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

import django.forms as forms
from django.http import QueryDict
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from whs.models import Seller, Agent, Pallet, Sold, Bill, Add, Inventory, Man, Sorting, Write_off, Brick, make_label, make_css
from whs.validation import validate_transfer


class DateForm(forms.Form):
    date = forms.DateField()

    @property
    def value(self):
        if self.is_valid():
            return self.cleaned_data['date']
        else:
            return datetime.date.today()

    def prev(self):
        return self.value - datetime.timedelta(1)
    def next(self):
        return self.value + datetime.timedelta(1)

    def prev_month(self):
        return self.value - relativedelta(months=1)
    def next_month(self):
        return self.value + relativedelta(months=1)


class NumberInput(forms.TextInput):
    input_type = 'number'


class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.legend = self.Meta.model._meta.verbose_name
        self.auto_id = 'doc_%s'

    class Meta:
        model = Bill
        verbose_name_accusative = u"Накладную"
        fields = ('date', 'number', 'agent', 'seller', 'reason', 'info')
        widgets = {
            'number': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'reason': forms.Textarea(attrs={'rows': 2}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }


class SoldForm(forms.ModelForm):
    class Meta:
        verbose_name = Sold._meta.verbose_name
        verbose_name_plural = Sold._meta.verbose_name_plural
        verbose_name_accusative = u"Отгрузку"
        model = Sold
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),
                   'tara': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'batch': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'price': NumberInput(attrs={'autocomplete': 'off', 'min': 1, 'step': 0.01}),
                   'delivery': NumberInput(attrs={'autocomplete': 'off', 'step': 0.01}),
                   'info': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        data = self.cleaned_data
        brick_from, brick, amount = data['brick_from'],data['brick'],data['amount']
        total = brick.total
        if brick_from:
            validate_transfer(brick_from,brick)
            total = brick_from.total
        if self.instance.pk:
            total +=self.instance.amount
        if total < amount:
            raise ValidationError(u'На складе нету столько кирпича')
        return data


class PalletForm(forms.ModelForm):
    class Meta:
        model = Pallet
        verbose_name = Pallet._meta.verbose_name
        verbose_name_plural = Pallet._meta.verbose_name_plural
        verbose_name_accusative = u"Поддон"

        widgets = {
            'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }

SoldFactory = inlineformset_factory(Bill, Sold, SoldForm, extra=0)
PalletFactory = inlineformset_factory(Bill, Pallet, PalletForm, extra=0)

class SoldFactory(SoldFactory):
    def clean(self):
        if any(self.errors):
            return
        bricks, amounts = {},{}
        for form in self.forms:
            brick_from, brick, amount = form.cleaned_data['brick_from'],form.cleaned_data['brick'],form.cleaned_data['amount']
            if brick_from:
                bricks[brick_from.pk] = brick_from
                amounts[brick_from.pk] = amounts.get(brick_from.pk,0) + amount
            else:
                bricks[brick.pk] = brick
                amounts[brick.pk] = amounts.get(brick.pk,0) + amount
            if form.instance.pk:
                amounts[brick.pk] -= form.instance.amount
        for pk in bricks:
            b = bricks[pk]
            if b.total < amounts[pk]:
                raise ValidationError(u'Не хватает кирпича для накладной, проверьте отгрузки по кирпичу %s' % b.label)

class YearMonthFilter(forms.Form):
    date__year = forms.IntegerField(required=True)
    date__month = forms.IntegerField(required=False)
    class Meta:
        dates = Bill.objects.dates('date','month')[::-1]

records_per_page = (
    (10,'10 записей на странице'),
    ('','20 записей на странице'),
    (50,'50 записей на странице'),
    (100,'100 записей на странице'),
)

class BillFilter(forms.Form):
    page = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    month = forms.IntegerField(required=False)
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), required=False)
    rpp = forms.ChoiceField(choices=records_per_page,initial='',required=False)

    def url_next(self):
        q = QueryDict('',mutable=True)
        if self.is_valid():
            q.update(self.cleaned_data.update(page=self.cleaned_data.get('page',1)+1))
        return q.urlencode()

    def url_prev(self):
        q = QueryDict('',mutable=True)
        if self.is_valid():
            q.update(self.cleaned_data.update(page=self.cleaned_data.get('page',2)-1))
        return q.urlencode()

    def __init__(self, *args, **kwargs):
        """ Изменение пустой ичейки для подсказки. """
        super(BillFilter, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'

    class Meta:
        dates = Bill.objects.dates('date','month').reverse()

bill_group_by = (
    ('seller',u'Продавцу'),
    ('agent',u'Покупателю'),
    ('brick',u'Кирпичу'),
    ('brick_from',u'Кирпичу перевода'),
)


class BillAggregateFilter(BillFilter):
    seller = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)
    group_by = forms.MultipleChoiceField(choices=bill_group_by)


class AgentForm(forms.ModelForm):
    class Meta:
        message = 'Внимательно заполняйте значения имя и полное имя.'
        model=Agent
        verbose_name_accusative =u'Контрагента'
        widgets = {
            'name': forms.Textarea(attrs=dict(rows=2)),
            'bank': forms.Textarea(attrs=dict(rows=2)),
            'address': forms.Textarea(attrs=dict(rows=2)),
            }

class SellerForm(forms.ModelForm):
    class Meta:
        message = 'Внимательно заполняйте значения имя и полное имя.'
        model=Seller
        verbose_name__accusative = u'Продавца'
        widgets = {
            'name': forms.Textarea(attrs=dict(rows=2)),
            'bank': forms.Textarea(attrs=dict(rows=2)),
            'address': forms.Textarea(attrs=dict(rows=2)),
            }


class AddForm(forms.ModelForm):
    class Meta:
        name = 'Add'
        model = Add
        fields = ('brick', 'amount')
        verbose_name = Add._meta.verbose_name
        verbose_name_plural = Add._meta.verbose_name_plural


class InventoryForm(forms.ModelForm):
    class Meta:
        name = 'Inventory'
        model = Inventory
        verbose_name = Inventory._meta.verbose_name
        verbose_name_plural = Inventory._meta.verbose_name_plural


class ManForm(forms.ModelForm):
    class Meta:
        name = 'Man'
        model = Man
        verbose_name = Man._meta.verbose_name
        verbose_name_plural = Man._meta.verbose_name_plural


class SortingForm(forms.ModelForm):
    class Meta:
        name = 'Sorting'
        model = Sorting
#        fields = ('brick', 'amount', 'poddon', 'tara', 'info')
        verbose_name = Sorting._meta.verbose_name
        verbose_name_plural = Sorting._meta.verbose_name_plural


class Write_offForm(forms.ModelForm):
    class Meta:
        name = 'Write_off'
        model = Write_off
        verbose_name = Write_off._meta.verbose_name
        verbose_name_plural = Write_off._meta.verbose_name_plural


AddFactory = inlineformset_factory(Man, Add, extra=0, form=AddForm, )
Write_offFactory = inlineformset_factory(Inventory, Write_off, extra=0, form=Write_offForm, )

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('name','nomenclature','cavitation','width','view','color','ctype','mark','defect','refuse','features',)
        exclude = ('total','css','label')
        widgets = {
            'name':         forms.TextInput(attrs={'class':'input-xxlarge'}),
            'nomenclature': forms.Select(attrs={'class':'input-xxlarge'}),
            }

    def clean(self):
        b = self.save(commit=False)
        try:
            b = Brick.objects.exclude(pk=b.pk).get(label=make_label(b))
        except Brick.DoesNotExist:
            return self.cleaned_data
        else:
            raise ValidationError(u'Такой кирпич вроде уже есть с УИД %d!' % b.pk)

class VerificationForm(forms.Form):
    csv = forms.FileField(label=u'Файл в формате csv')
    id = forms.IntegerField(initial=1,label=u'Номер столбца с УИД')
    field = forms.IntegerField(initial=10,label=u'Номер столбца для сверки')