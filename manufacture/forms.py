# -*- coding: utf-8 -*-
__author__ = 'bteam'
import dojango.forms as forms
from whs.manufacture.models import *

class ManForm(forms.ModelForm):
    class Meta:
        model=Man
        exclude=('draft',)
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}


  