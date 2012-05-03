# -*- coding: utf-8 -*-
import django.forms as forms
from django.core.exceptions import ValidationError

from whs.brick.models import Brick, make_label

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('name','nomenclature','weight','view','color','ctype','mark','defect','refuse','features',)
        exclude = ('total','css','label')
        widgets = {
            'name':         forms.TextInput(attrs={'class':'input-xxlarge'}),
            'nomenclature': forms.Select(attrs={'class':'input-xxlarge'}),
            }

    def clean(self):
        b = self.save(commit=False)
        if Brick.objects.filter(label=make_label(b)).count():
            raise ValidationError(u'Такой кирпич вроде уже есть!')
        return self.cleaned_data
