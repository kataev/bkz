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

class Device(models.Model):
    name = models.CharField(u'Имя устройства',max_length=100)
    code = models.CharField(u'Код устройства',max_length=100)

    def __unicode__(self):
        return self.name + self.code

pos = {
    101:4,
    102:4.66,
    103:5.33,
    201:6.66,
    202:7.33,
    203:8,
    204:8.66,
    205:9.33,
    206:10,
    207:10.66,
    208:11.33,
    303:12.66,
    304:13.66,
    305:14.66
}

line = {101: 19,
        102: 20,
        103: 21,
        201: 10,
        202: 11,
        203: 12,
        204: 13,
        205: 14,
        206: 15,
        207: 16,
        208: 17,
        303: 22,
        304: 23,
        305: 24}

class Position(models.Model):
    name = models.ForeignKey(Device,verbose_name=u'Имя устройства')
    field = models.CharField(u'Канал устойства',max_length=100,null=True,blank=True)
    place = models.CharField(u'Раположение',max_length=50,choices=places,null=True,blank=True)
    unit = models.CharField(u'Еденицы измерения',max_length=50,null=True,blank=True,choices=unit_c)
    label = models.CharField(u'Имя',max_length=50)
    position = models.FloatField(u'Позиция',max_length=100)

    class Meta:
        verbose_name=u'позиция точек и датчиков'
        verbose_name_plural=u'позиции точек и датчиков'


class Value(models.Model):
    code = models.IntegerField(u'Номер в сети ModBus')
    field = models.IntegerField(u'Номер канала')
    value = models.FloatField(u'Значение')
    datetime = models.DateTimeField(auto_now=True)