# -*- coding: utf-8 -*-
import pytils

from django.db import models
from django.core.urlresolvers import reverse

class Energy(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    elec4=models.FloatField(u"Электр 4 ячейка")
    elec16=models.FloatField(u"Электр 16 ячейка")
    iwater=models.FloatField(u"Пром. Вода")
    uwater=models.FloatField(u"Хоз. Вода")
    gaz=models.PositiveIntegerField(u"Газ нм³")

    class Meta():
        verbose_name = u"Энергоресурсы"
        verbose_name_plural = u"Энергоресурсы"
        ordering = ('-date',)

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'%s' % date
        else:
            return u'Новые показания энергоресурсов'

    def get_absolute_url(self):
        return reverse('energy:Energy-pk',kwargs=dict(id=self.pk or ''))


class Teplo(models.Model):
    date_time=models.DateTimeField(u"Дата и время",auto_now=True)
    date=models.DateField(u"Дата")
    henergy=models.FloatField(u"ТЭнергия кал")
    hot_water=models.FloatField(u"Расход гор.воды м³")
    rpr=models.FloatField(u"Давл прих кг/см²")
    robr=models.FloatField(u"Давл уход кг/см²")
    tpr=models.FloatField(u"Темп прих С°")
    tobr=models.FloatField(u"Темп обр С°")

    class Meta():
        verbose_name = u"Тепло"
        verbose_name_plural = u'Тепло'
        ordering = ('-date',)
    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'%s' % date
        else:
            return u'Новые показания тепла'

    def get_absolute_url(self):
        return reverse('energy:Teplo-pk',kwargs=dict(id=self.pk or ''))