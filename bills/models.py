# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from whs.bricks.models import bricks
from django.db import models
from dojango.forms import ModelForm
from dojango.forms import DateField,DateInput
from dojango.data.modelstore import  *
from dojango.forms import ModelChoiceField

class sold(oper):
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
        model=sold


class transfer(oper):
#    brick_from=models.ForeignKey(bricks,related_name='from',verbose_name=u'Откуда',help_text=u'Из какого кирпича')
#    brick=models.ForeignKey(bricks,related_name='to',verbose_name=u'Куда',help_text=u'В какой')
#    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Число, больше остатка')
#    time_change=models.DateTimeField(auto_now=True)
    sold = models.ManyToManyField(sold,blank=True,null=True,help_text=u'продажа')
    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = "Переводы"

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class transferForm(ModelForm):
    class Meta:
        model=transfer

## Отгрузка


## Накладная
class bill(doc):
    solds = models.ManyToManyField(sold,blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfers = models.ManyToManyField(transfer,blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"Накладная"
            verbose_name_plural = u"Накладные"

    def __unicode__(self):
        return 'Накладная %d' % self.id

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class billForm(ModelForm):
    class Meta:
        model=bill

#class billStore(Store):
##    id = StoreField()
#    number = StoreField()
#    doc_date = StoreField( get_value=ValueMethod('strftime', '%Y-%m-%d') )
#    info = StoreField()
##    time_change = StoreField( get_value=ValueMethod('__str__') )
#    solds = ReferenceField()
#    transfers = ReferenceField()
#
#
#    class Meta(object):
#        objects = bills.objects.all()
##        label = bricks._meta.verbose_name
