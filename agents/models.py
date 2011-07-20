# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm, Textarea

class agent(models.Model):

    type_c = ((0,u'Обычный покупатель'),(1,u'Строительная компания'))

    name=models.CharField(u"Имя",max_length=200)
    form=models.CharField(u"Юр форма",blank=True,max_length=200)
    type=models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)
    address=models.CharField(u"Адресс",blank=True,max_length=200)
    bank=models.CharField(u"Банк",blank=True,max_length=200)
    phone=models.CharField(u"Телефон",blank=True,max_length=200)
    inn=models.CharField(u"Инн",blank=True,max_length=200)
    account=models.CharField(u"Счет",blank=True,max_length=200)

    def bills(self):
        return u'/bills/?agent=%s' % self.id


    class Meta:
        verbose_name=u'КонтрАгент'
        verbose_name_plural=u'КонтрАгенты'

    def __unicode__(self):
        return u'%s, %s' % (self.name,self.form)



class agentForm(ModelForm):
    class Meta:
        model=agent
        widgets = {
            'bank': Textarea(attrs={}),
            'address': Textarea(attrs={}),
        }

class agent_filter_form(ModelForm):
    class Meta:
        model=agent
        field = ['name','form','type','address','inn']
