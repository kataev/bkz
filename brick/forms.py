# -*- coding: utf-8 -*-
import django.forms as forms
from whs.brick.models import Brick

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label')
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}
