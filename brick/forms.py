# -*- coding: utf-8 -*-
import django.forms as forms

from whs.brick.models import Brick


class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('name','nomenclature','weight','view','color','ctype','mark','defect','refuse','features',)
        exclude = ('total','css','label')
        widgets = {
            'name':         forms.TextInput(attrs={'class':'input-xxlarge'}),
            'nomenclature': forms.Select(attrs={'class':'input-xxlarge'}),
            }