# -*- coding: utf-8 -*-
import django.forms as forms
from django.core.exceptions import ValidationError

from whs.brick.models import Brick, make_label

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
            pass
        else:
            raise ValidationError(u'Такой кирпич вроде уже есть с УИД %d!' % b.pk)
        return self.cleaned_data


class VerificationForm(forms.Form):
    csv = forms.FileField(label=u'Файл в формате csv')
    id = forms.IntegerField(initial=1,label=u'Номер столбца с УИД')
    field = forms.IntegerField(initial=10,label=u'Номер столбца для сверки')