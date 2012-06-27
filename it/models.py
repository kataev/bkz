# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime

class Device(models.Model):
    name = models.CharField(u'Имя', max_length=300)
    place = models.CharField(u'Местоположение', max_length=300, blank=True)
    type = models.ForeignKey('self',null=True, blank=True, verbose_name=u'Тип')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    def __unicode__(self):
        if self.pk:
            if self.type and self.place:
                return u'%s,\t%s' % (self.name,self.place)
            else:
                return self.name
        else:
            return u'Новый девайс'

    def get_absolute_url(self):
        if self.type:
            return reverse('it:Device',kwargs=dict(id=self.id))
        else:
            return reverse('it:main')

    class Meta:
        verbose_name = u"Устройство"
        verbose_name_plural = u"Уствойства"

class Buy(models.Model):
    cartridge = models.ForeignKey(Device,verbose_name=u'Картридж')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())
    amount = models.PositiveIntegerField(u"Кол-во", help_text=u'Кол-во')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт.')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    def __unicode__(self):
        if self.pk:
            return u'%s купленно %s' % (self.cartridge,self.date)
        else:
            return u'Новые расходники'

    def get_absolute_url(self):
        return reverse('it:Buy',kwargs=dict(id=self.id))

    def total(self):
        return self.price * self.amount

    class Meta:
        verbose_name = u"Расходники"
        verbose_name_plural = u"Расходники"
        ordering = ['-date']

class Plug(models.Model):
    cartridge = models.ForeignKey(Buy,verbose_name=u'Расходник',related_name=u'plug')
    printer = models.ForeignKey(Device,verbose_name=u'Устройство',related_name=u'printer')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())

    def __unicode__(self):
        if self.pk:
            return u'у %s от %s' % (self.cartridge,self.date)
        else:
            return u'Установлен расходник'

    def get_absolute_url(self):
        return reverse('it:Plug',kwargs=dict(id=self.id))
    class Meta:
        verbose_name = u'Замена'
        verbose_name_plural = u'Замены'

statuses = (
    (u'info',u'Созданно'),
    (u'warning',u'В работе'),
    (u'success',u'Завершенно'),
)

class Work(models.Model):
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

    def get_absolute_url(self):
        return reverse('it:Work',kwargs=dict(id=self.id))

    class Meta:
        verbose_name = u"Заявка"
        verbose_name_plural = u"Заявки"
        ordering = ['-date']

