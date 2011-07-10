# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from whs.bricks.models import bricks
from django.db import models
from dojango.forms import ModelForm
from dojango.forms import DateField,DateInput
from dojango.data.modelstore import  *
from dojango.forms import ModelChoiceField
import pytils

class sold(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"
            verbose_name_plural =  u"Отгрузки"

    def __unicode__(self):
        return u'Отгрузка %s, %d шт' % (self.brick,self.amount)

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)


    def def save(self, *args, **kwargs):
    
        super(Blog, self).save(*args, **kwargs)

class soldForm(ModelForm):
    class Meta:
        model=sold


class transfer(oper):
    sold = models.ForeignKey(sold,blank=True,null=True,verbose_name=u'Отгрузка')
    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = "Переводы"

    def __unicode__(self):
        if self.sold is None:
            return u'Незаконченный перевод из %s, %d шт' % (self.brick,self.amount)
        else:
            return u'Перевод из %s в %s, %d шт' % (self.brick,self.sold.brick,self.amount)

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
        return u'Накладная № %d от %s' % (self.number,pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc_date))

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class billForm(ModelForm):
    class Meta:
        model=bill