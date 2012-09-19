# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from bkz.utils import UrlMixin,ru_date

class Device(models.Model,UrlMixin):
    name = models.CharField(u'Имя', max_length=300)
    place = models.CharField(u'Местоположение', max_length=300, blank=True)
    type = models.ForeignKey('self',null=True, blank=True, verbose_name=u'Тип')
    value = models.IntegerField(u'Числовая характеристика')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    def __unicode__(self):
        if self.pk:
            return u'%s\t%s' % (self.name,self.place)
        else:
            return u'Новый девайс'

    class Meta:
        verbose_name = u"Устройство"
        verbose_name_plural = u"Уствойства"
        ordering = ('type__name',)

class Buy(models.Model,UrlMixin):
    cartridge = models.ForeignKey(Device,verbose_name=u'Картридж',related_name=u'buy')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())
    amount = models.PositiveIntegerField(u"Кол-во", help_text=u'Кол-во')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт.')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    def __unicode__(self):
        if self.pk:
            return u'%s от %s, %.2f' % (self.cartridge,ru_date(self.date),self.price)
        else:
            return u'Новые расходники'

    def total(self):
        return self.price * self.amount

    class Meta:
        verbose_name = u"Накладная по покупке расходников"
        verbose_name_plural = u"Накладные по покупке расходников"
        ordering = ['-date']

class Plug(models.Model,UrlMixin):
    bill = models.ForeignKey(Buy,verbose_name=u'Расходник',related_name=u'plug')
    printer = models.ForeignKey(Device,verbose_name=u'Устройство',related_name=u'plug')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())

    def __unicode__(self):
        if self.pk:
            return u'у %s от %s' % (self.bill,self.date)
        else:
            return u'Установлен расходник'

    class Meta:
        verbose_name = u'Замена'
        verbose_name_plural = u'Замены'
        ordering = ('date',)

statuses = (
    (u'info',u'Созданно'),
    (u'warning',u'В работе'),
    (u'success',u'Завершенно'),
)

class Work(models.Model,UrlMixin):
    device = models.ForeignKey(Device,verbose_name=u'Устройство',null=False,blank=False)
    name = models.CharField(u'Описание проблемы', max_length=300)
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())
    people = models.ForeignKey(User,verbose_name=u'Человек', null=True, blank=True)
    status = models.CharField(u'Статус', max_length=300, choices=statuses,default=u'info')
    date_finished = models.DateField(u'Дата выполнения', null=True, blank=True)

    def __unicode__(self):
        if self.pk:
            return u'%s на %s'% (self.name,self.device)
        else:
            return u'Новая заявка'

    class Meta:
        verbose_name = u"Заявка"
        verbose_name_plural = u"Заявки"
        ordering = ['-date']

