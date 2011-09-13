# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.brick.models import Brick,History

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total',)
    class Media:
        js = ('form.js',)
        css = {'all':('form.css',),}
