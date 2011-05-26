# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from whs.bricks.models import bricks
from django.db import models
from dojango.forms import ModelForm
from dojango.forms import DateField,DateInput

class solds(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"
            verbose_name_plural =  u"Отгрузка"

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class soldForm(ModelForm):
    class Meta:
        model=solds



class transfers(models.Model):
    brick_from=models.ForeignKey(bricks,related_name='from',verbose_name=u'Откуда',help_text=u'Из какого кирпича')
    brick_to=models.ForeignKey(bricks,related_name='to',verbose_name=u'Куда',help_text=u'В какой')
    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Число, больше остатка')
    time_change=models.DateTimeField(auto_now=True)
    solds = models.ManyToManyField(solds,blank=True,null=True,help_text=u'продажа')
    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = "Переводы"

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class transferForm(ModelForm):
    class Meta:
        model=transfers

## Отгрузка


## Накладная
class bills(doc):
    solds = models.ManyToManyField(solds,blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"Накладная"
            verbose_name_plural = u"Накладные"

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class billForm(ModelForm):
    class Meta:
        model=bills