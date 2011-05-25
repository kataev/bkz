# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from whs.bricks.models import bricks
from django.db import models
from dojango.forms import ModelForm

class transfers(models.Model):
    brick_from=models.ForeignKey(bricks,related_name='from',verbose_name=u'Откуда',help_text=u'Из какого кирпича')
    brick_to=models.ForeignKey(bricks,related_name='to',verbose_name=u'Куда',help_text=u'В какой')
    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Число, больше остатка')
    time_change=models.DateTimeField(auto_now=True)
    class Meta():
            verbose_name = u"Перевод"

#    def __unicode__(self):
#        return 'Transfer %i' %self.pk

class transferForm(ModelForm):
    class Meta:
        model=transfers

## Отгрузка
class solds(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"

    #def __unicode__(self):
    #    return u'id '+str(self.id)

class soldForm(ModelForm):
    class Meta:
        model=solds

## Накладная
class bills(doc):
    solds = models.ManyToManyField(solds,blank=True,null=True,help_text=u'Отгрузки')
    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Переводы')

    class Meta():
            verbose_name = u"Накладная"

class billForm(ModelForm):
    class Meta:
        model=bills
#        widgets = {
#            'draft': CheckboxInput(attrs={'value': True})
#        }