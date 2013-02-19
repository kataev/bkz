# -*- coding: utf-8 -*-
from django.db import models

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

class CpuDevice(models.Model):
    name = models.CharField(u'Имя устройства',max_length=100)
    code = models.CharField(u'Код устройства',max_length=100)

    class Meta:
        verbose_name=u'Устройство'
        verbose_name_plural=u'Устройства'

    def __unicode__(self):
        return self.name + self.code

positions = {
    101:4,    # Зона нагревания
    102:4.66,
    103:5.33, 

    201:6.66, # Обжиг
    202:7.33,
    203:8,
    204:8.66,
    205:9.33,
    206:10,
    207:10.66,
    208:11.33,

    303:12.66, # Охлаждение
    304:13.66,
    305:14.66
}

line = {10: 201,
        11: 202,
        12: 203,
        13: 204,
        14: 205,
        15: 206,
        16: 207,
        17: 208,
        19: 101,
        20: 102,
        21: 103,
        22: 303,
        23: 304,
        24: 305}

class Position(models.Model):
    name = models.ForeignKey(CpuDevice,verbose_name=u'Имя устройства')
    field = models.CharField(u'Канал устойства',max_length=100,null=True,blank=True)
    place = models.CharField(u'Расположение',max_length=50,choices=places,null=True,blank=True)
    unit = models.CharField(u'Еденицы измерения',max_length=50,null=True,blank=True,choices=unit_c)
    label = models.CharField(u'Имя',max_length=50)
    position = models.FloatField(u'Позиция',max_length=100)

    @property
    def path(self):
        return 'cpu.%s.%s' % (self.name.code,self.field)

    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.name,self.field,self.unit,self.place,self.position)

    class Meta:
        verbose_name=u'позиция точек и датчиков'
        verbose_name_plural=u'позиции точек и датчиков'