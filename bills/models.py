# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from django.db import models
from dojango.forms import ModelForm
#from dojango.forms import DateField,DateInput
#from dojango.data.modelstore import  *
#from dojango.forms import ModelChoiceField
import pytils
#from django.contrib.contenttypes.models import ContentType
#from django.db.models.signals import pre_save
#from django.dispatch import receiver
#from django.contrib.admin.models import LogEntry, ADDITION

class sold(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"
            verbose_name_plural =  u"Отгрузки"

    def __unicode__(self):
        return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)


class soldForm(ModelForm):
    class Meta:
        model=sold
        exclude=('post')

class transfer(oper):
    sold = models.ForeignKey(sold,blank=True,null=True,verbose_name=u'Отгрузка') #Куда
    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = "Переводы"

    def __unicode__(self):
        if self.sold is None:
            return u'Незаконченный перевод № %d из %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Перевод № %d из %s в %s, %d шт' % (self.pk,self.brick,self.sold.brick,self.amount)

    def get_absolute_url(self):
        return "/json/%s/%i/" % (self._meta.module_name,self.id)

class transferForm(ModelForm):
    class Meta:
        model=transfer
        exclude=('post')

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

    def posting(self):
        transfers = self.transfers.all()
        solds = self.solds.all()

        errors= []
        for t in transfers: # Обрабатываем
            t.brick.total +=t.amount
            t.sold.brick.total -= t.amount
        for s in solds:
            s.brick.total -=s.amount

        for t in transfers: # Проверяем
            if t.brick.total < 0:
                error = {'brick':t.brick,'amount':t.brick.total*-1,'error':u'Не хватает кирпича','oper':t}
                errors.append(error)
            if t.sold.brick.total < 0:
                error = {'brick':t.sold.brick,'amount':t.sold.brick.total*-1,'error':u'Не хватает кирпича в принимащей строне',"oper":t}
                errors.append(error)
        for s in solds:
            if s.brick.total < 0:
                error = {'brick':s.brick,'amount':s.brick.total*-1,'error':u'Не хватает кирпича','oper':s}
                errors.append(error)
        if len(errors) > 0:
            return errors
        else:
            for t in transfers:
                t.brick.save()
                t.sold.brick.save()
                t.post=True

            for s in solds:
                s.brick.save()
                s.post=True
            self.draft=True
            return []



class billForm(ModelForm):
    class Meta:
        model=bill
        exclude=('draft')