# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.loading import get_models

places = (
    (u'firing',u'Обжиг'),
    (u'drying_1',u'Сушка 1'),
    (u'drying_2',u'Сушка 2'),
)

unit_c = (
    (u'temp',u'температура'),
    (u'hmdt',u'влажность'),
    (u'p',u'давление'),
    (u'dep',u'разряжение'),
)

class Devices(models.Model):
    name = models.CharField(u'Имя устройства',max_length=100)
    code = models.CharField(u'Код устройства',max_length=100)

    def __unicode__(self):
        return self.name

class Positions(models.Model):
    name = models.ForeignKey(Devices,verbose_name=u'Имя устройства')
    field = models.CharField(u'Канал устойства',max_length=100,null=True,blank=True)
    place = models.CharField(u'Раположение',max_length=50,choices=places,null=True,blank=True)
    unit = models.CharField(u'Еденицы измерения',max_length=50,null=True,blank=True,choices=unit_c)
    position = models.CharField(u'Позиция',max_length=100)

    def show(self):
        return dict(field=self.field,place=self.get_place_display(),position=self.position)

    class Meta:
        verbose_name=u'позиция точек и датчиков'
        verbose_name_plural=u'позиции точек и датчиков'

    def __unicode__(self):
        if self.field:
            name = u'%s %s' % (self.name,self.field)
        else:
            name = self.name.name
        if self.place:
            return u'%s в %s %s' % (name,self.get_place_display(),self.position)
        else:
            return u'%s %s' % (name,self.position)
