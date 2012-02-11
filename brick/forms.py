# -*- coding: utf-8 -*-
import django.forms as forms
from whs.brick.models import Brick

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label','sold','begin','add','t_from','t_to')
        widgets = {
            'name': forms.Textarea(attrs=dict(rows=2)),
            }
    class Media:
        pass