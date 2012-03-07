# -*- coding: utf-8 -*-
import django.forms as forms

from whs.brick.models import Brick


class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('name','color','mark','weight','view','ctype','defect','refuse','features',)
        exclude = ('total','css','label')
        widgets = {
            'name': forms.Textarea(attrs={'rows':2,'class':'input-xlarge'}),
            }