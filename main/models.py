# -*- coding: utf-8 -*-
from django.db import models
from whs.bricks.models import bricks
from whs.agents.models import agent
from dojango import forms

#class BrickWidget(model.ForeignKey)

class bills_filter_form(forms.Form):
    date1 = forms.DateField(required=False,widget=forms.DateInput(attrs={'style':'width:90px;'}),help_text=u'Дата или начало периода')
    date2 = forms.DateField(required=False,widget=forms.DateInput(attrs={'style':'width:90px;'}),help_text=u'Конец периода')
    brick = forms.ModelChoiceField(required=False,queryset=bricks.objects.all(),help_text=u'Кирпич')
    agent = forms.ModelChoiceField(required=False,queryset=agent.objects.all(),widget=forms.FilteringSelect(attrs={'style':'width:160px;'}),help_text=u'Контрагент')
    number = forms.CharField(required=False,widget=forms.NumberSpinnerInput(attrs={'style':'width:80px;','constraints':{'min':1}}),help_text=u'Номер накладной')

class oper(models.Model):

    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))

#    post_c=((False,u'Не проведенно'),(True,u'Проведенно'))
    brick=models.ForeignKey(bricks,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
    amount=models.PositiveIntegerField(u"Кол-во кирпича",help_text=u'Кол-во кирпича для операции')
    tara=models.PositiveIntegerField(u"Кол-во поддонов",default=0)
    poddon=models.PositiveIntegerField(u"Тип поддона",choices=poddon_c,default=1)
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
    post=models.BooleanField(u'Проведенно?',default=False)
    # DRAFT ДЛЯ ПРОСТОТЫ!!!! ПОДУМАТЬ!!!

    class Meta:
        abstract = True


class doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))
    
    number=models.PositiveIntegerField(unique=True,verbose_name=u'№ документа',help_text=u'Число')
    doc_date=models.DateField(u'Дата',help_text=u'Дата документа')
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
#    time_change=models.DateTimeField(auto_now=True)
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True
