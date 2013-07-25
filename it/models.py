# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from bkz.utils import UrlMixin, ru_date


class Device(models.Model, UrlMixin):
    name = models.CharField(u'Имя', max_length=300)
    place = models.CharField(u'Местоположение', max_length=300, blank=True)
    type = models.ForeignKey('self', null=True, blank=True, verbose_name=u'Тип')
    value = models.IntegerField(u'Числовая характеристика')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')
    allowed = models.ManyToManyField('self', verbose_name=u'Девайс', null=True, blank=True)

    @property
    def avg_demand(self):
        plugs = self.plug.order_by('date').all()
        values = []
        if len(plugs) > 1:
            v, d = None, None
            for p in plugs:
                if not d and not v:
                    d = p.date
                    v = p.bill.cartridge.value
                else:
                    values.append((v, p.date - d))
            a = [x[0] / x[1].days for x in values]
            return sum(a) / len(a)

    def __unicode__(self):
        if self.pk:
            return u'%s\t%s' % (self.name, self.place)
        else:
            return u'Новый девайс'

    class Meta:
        verbose_name = u"Устройство"
        verbose_name_plural = u"Уствойства"
        ordering = ('type__name', 'place', 'name')


class Buy(models.Model, UrlMixin):
    cartridge = models.ForeignKey(Device, verbose_name=u'Картридж', related_name=u'buy')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())
    amount = models.PositiveIntegerField(u"Кол-во", help_text=u'Кол-во')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт.')
    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    def __unicode__(self):
        if self.pk:
            return u'%s от %s, %.2f' % (self.cartridge, ru_date(self.date), self.price)
        else:
            return u'Новые расходники'

    def total(self):
        return self.price * self.amount

    class Meta:
        verbose_name = u"Накладная по покупке расходников"
        verbose_name_plural = u"Накладные по покупке расходников"
        ordering = ('-date',)


class Plug(models.Model, UrlMixin):
    bill = models.ForeignKey(Buy, verbose_name=u'Расходник', related_name=u'plug')
    printer = models.ForeignKey(Device, verbose_name=u'Устройство', related_name=u'plug')
    date = models.DateField(u'Дата', help_text=u'Дата', default=datetime.date.today())

    def __unicode__(self):
        if self.pk:
            return u'у %s от %s' % (self.bill, self.date)
        else:
            return u'Установлен расходник'

    class Meta:
        verbose_name = u'Замена'
        verbose_name_plural = u'Замены'
        ordering = ('-date',)
