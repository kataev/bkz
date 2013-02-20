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

target ={101: [437, 444, 451, 458, 465, 472, 479],
         102: [469, 478, 487, 496, 505, 514, 523],
         103: [533, 540, 548, 555, 563, 570, 578],
         201: [592, 599, 606, 613, 620, 627, 634],
         202: [725, 730, 735, 740, 745, 750, 755],
         203: [795, 800, 805, 810, 815, 820, 825],
         204: [865, 870, 875, 880, 885, 890, 895],
         205: [935, 940, 945, 950, 955, 960, 965],
         206: [973, 976, 979, 982, 985, 988, 991],
         207: [982, 984, 986, 988, 990, 992, 994],
         208: [935, 940, 945, 950, 955, 960, 965],
         302: [808, 816, 824, 832, 840, 848, 856],
         303: [707, 714, 721, 728, 735, 742, 749],
         304: [567, 574, 581, 588, 595, 602, 609],
         305: [408, 416, 424, 432, 440, 448, 456]}


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