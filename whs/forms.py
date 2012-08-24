# -*- coding: utf-8 -*-
from collections import defaultdict

import django.forms as forms
from bootstrap.forms import BootstrapMixin
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from whs.models import *
from whs.validation import validate_transfer

from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.html import escape

class AgentSelect(forms.Select):
    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        letter = u''
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                current_letter = option_label[0:1].capitalize()
                if letter != current_letter:
                    output.append(u'<optgroup label="%s">' % escape(force_unicode(current_letter)))
                    output.append(self.render_option(selected_choices, option_value, option_label))
                    output.append(u'</optgroup>')
                else:
                    output.append(self.render_option(selected_choices, option_value, option_label))
                letter = current_letter
        return u'\n'.join(output)

class BrickSelect(forms.widgets.Input):
    input_type = 'hidden'

class NumberInput(forms.TextInput):
    input_type = 'number'
    def __init__(self, attrs=None):
        super(NumberInput,self).__init__(attrs=attrs)
        self.attrs['autocomplete'] = 'off'

class BatchInput(forms.TextInput):
    input_type = 'number'
    def __init__(self, attrs=None):
        super(BatchInput,self).__init__(attrs=attrs)
        self.attrs['step'] = 1
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'

class DateInput(forms.TextInput):
    input_type = 'date'

class TaraInput(forms.TextInput):
    input_type = 'number'
    def __init__(self, attrs=None):
        super(TaraInput,self).__init__(attrs=attrs)
        self.attrs['step'] = 1
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'


class MoneyInput(forms.TextInput):
    input_type = 'number'
    def __init__(self, attrs=None):
        super(MoneyInput,self).__init__(attrs=attrs)
        self.attrs['step'] = 0.01
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'


class DateForm(forms.Form):
    date = forms.DateField()

class BillForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('date', 'number', 'agent', 'seller', 'reason', 'info')
        widgets = {
            'date':DateInput,
            'number':NumberInput(attrs={'min':1,'step':1}),
            'agent':AgentSelect,
            'seller':AgentSelect,
            'info':forms.Textarea(attrs={'rows':1}),
        }

class SoldForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Sold
        widgets = {
            'brick':BrickSelect,
            'brick_from':BrickSelect,
            'batch_number':BatchInput(attrs={'placeholder':'Номер',}),
            'batch_year':BatchInput(attrs={'placeholder':'Год',}),
            'tara':TaraInput,
            'amount':NumberInput,
            'price':MoneyInput,
            'delivery':MoneyInput,
            'info':forms.Textarea(attrs={'rows':1}),
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


class PalletForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Pallet
        widgets = {
            'amount':NumberInput,
            'price':MoneyInput,
            'info':forms.Textarea(attrs={'rows':1}),
            }


SoldFactory = inlineformset_factory(Bill, Sold, SoldForm, extra=0)
PalletFactory = inlineformset_factory(Bill, Pallet, PalletForm, extra=0)

class SoldFactory(SoldFactory):
    select_related = ('brick', 'brick_from')
    def get_queryset(self):
        return self.model.objects.select_related(*self.select_related)

    def clean(self):
        if any(self.errors):
            return
        bricks, amounts = {},defaultdict(int)
        for form in self.forms:
            if not form.cleaned_data: continue
            if form.cleaned_data.get('brick_from',None):
                id = form.cleaned_data['brick_from'].pk
            else:
                id = form.cleaned_data['brick'].pk
            amounts[id] += form.cleaned_data['amount']
            if form.instance.pk:
                amounts[id] -= form.instance.amount
        for id in bricks:
            b = bricks[id]
            if b.total < amounts[id]:
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
        model=Agent

agent_choices = (
    (0,'Выбрать'),
    (1,'Создать'),
)

class AgentCreateOrSelectForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False,)

class SellerForm(forms.ModelForm):
    class Meta:
        model=Seller

class AddForm(forms.ModelForm):
    class Meta:
        model = Add

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory

class SortingForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Sorting
        exclude = ('source',)
        widgets = {
            'date':DateInput,
            'brick':BrickSelect,
            'amount':NumberInput,
            'info':forms.Textarea(attrs={'rows':1}),
            }

class SortedForm(SortingForm):
    class Meta(SortingForm.Meta):
        exclude = ('source','part')

class BrockenForm(SortingForm):
    class Meta(SortingForm.Meta):
        exclude = ('source','part')

SortingFactory = inlineformset_factory(Sorting, Sorting,form=SortingForm,extra=0)

class SortedFactory(SortingFactory):
    select_related = tuple()
    form = SortedForm

    def get_queryset(self):
        return self.model.objects.select_related(*self.select_related).filter(source__isnull=False, part__isnull=False)

    @classmethod
    def get_default_prefix(cls):
        return 'sorted'

class BrockenFactory(SortingFactory):
    select_related = tuple()
    form = BrockenForm

    def get_queryset(self):
        return self.model.objects.select_related(*self.select_related).filter(source__isnull=False, part__isnull=True)

    @classmethod
    def get_default_prefix(cls):
        return 'brocken'

class Write_offForm(forms.ModelForm):
    class Meta:
        model = Write_off

Write_offFactory = inlineformset_factory(Inventory, Write_off, extra=0, form=Write_offForm, )

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label')

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