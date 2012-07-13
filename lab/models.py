# -*- coding: utf-8 -*-
import re

from django.core.validators import RegexValidator
from django.utils import datetime_safe as datetime
from django.core.urlresolvers import reverse
from django.db import models

from whs.brick.constants import defect_c,color_c

slash_separated_float_list_re = re.compile('^([-+]?\d*\.|,?\d+[/\s]*)+$')
validate_slash_separated_float_list = RegexValidator(slash_separated_float_list_re,u'Вводите числа разеделённые дробью','invalid')

from south.modelsinspector import add_introspection_rules




class SlashSeparatedFloatField(models.CharField):
    default_validators = [validate_slash_separated_float_list]
    description = u'Slash-separated floats'

    def formfield(self,**kwargs):
        defaults = {
            'error_messages': {
                'invalid': u'Вводите числа разеделённые дробью'
            }
        }
        defaults.update(kwargs)
        return super(SlashSeparatedFloatField,self).formfield(**defaults)

add_introspection_rules([],["^whs\.lab\.models\.SlashSeparatedFloatField"])

class Clay(models.Model):
    datetime = models.DateTimeField(u'Дата', default=datetime.datetime.now())
    humidity = SlashSeparatedFloatField(u'Пробы влажности',max_length=300)
    sand = models.FloatField(u'Песок %')
    inclusion = models.FloatField(u'Включения %')
    dust = models.FloatField(u'Пылеватость %')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def get_absolute_url(self):
        return reverse('lab:Clay-view',kwargs=dict(id=self.pk))

    def __unicode__(self):
        return u'%s' % self.datetime

    class Meta():
        verbose_name = u"Проба глины из карьера"

clay_positions = (
    (1,u'Позиция 1'),
    (2,u'Позиция 2'),
    (3,u'Позиция 3'),
    (4,u'Позиция 4'),
    (5,u'Позиция 5'),
)

class StoredClay(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    position = models.CharField(u'Позиция',max_length=30,choices=clay_positions,default=1)
    humidity = models.FloatField(u'Влажность')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Глина по позициям"

class Sand(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    humidity = models.FloatField(u'Влажность')
    particle_size = models.FloatField(u'Гран. состав')
    module_size = models.FloatField(u'Модуль крупности')
    dirt = models.TextField(u'Включения')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Песок"


width_c = (
    (0.8,u'КЕРПу'),
    (1.0,u'КОРПу'),
    (1.4,u'КУРПу'),
)

class Bar(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    width = models.CharField(u'Вид бруса',choices=width_c,default=1.0,max_length=30)
    tts = models.CharField(u'Номер ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    weight = models.FloatField(u'Масса')
    temperature = models.FloatField(u'Температура')
    humidity = models.FloatField(u'Влажность')
    sand = models.FloatField(u'Влажность')
    poke_left = models.CommaSeparatedIntegerField(u'Тычок левый',max_length=300)
    poke_right = models.CommaSeparatedIntegerField(u'Тычок правый',max_length=300)
    stratcher_left = models.CommaSeparatedIntegerField(u'Ложок левый',max_length=300)
    stratcher_right = models.CommaSeparatedIntegerField(u'Ложок правый',max_length=300)
    cutter = models.CommaSeparatedIntegerField(u'Отрезчик',max_length=3000)
    humidity_transporter = models.FloatField(u'Влажность с конвейера')
    info = models.TextField(u'Примечание',max_length=3000)

    class Meta():
        verbose_name = u"Брус"

class Raw(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    tts = models.CharField(u'Номер ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    temperature = models.FloatField(u'Температура')
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Сырец из накопителя"

class Half(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    position = models.IntegerField(u'Позиция')
    path = models.IntegerField(u'Путь')
    width = models.CharField(u'Вид бруса',max_length=30)
    size = models.CharField(u'Размер',max_length=20)
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    shrink = models.FloatField(u'Усадка')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Полуфабрикат"

class WaterAbsorption(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30,choices=color_c)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Водопоглащение"

class Efflorescence(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Высолы"

class FrostResistance(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Морозостойкость"

class Density(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Плотность"

class Batch(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    tto = models.CharField(u'Номер ТТО',max_length=20)
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30,choices=color_c)
    water_absorption = models.ForeignKey(WaterAbsorption, verbose_name=u'Водопоглащение', null=True, blank=True)
    efflorescence = models.ForeignKey(Efflorescence, verbose_name=u'Высолы', null=True, blank=True)
    frost_resistance = models.ForeignKey(FrostResistance, verbose_name=u'Морозостойкость', null=True, blank=True)
    density = models.ForeignKey(Density,verbose_name=u'Плотность')
    inclusion = models.TextField(u'Включения')
    mark = models.PositiveIntegerField(u"Марка")
    chamfer = models.IntegerField(u'Фаска',max_length=300)
    info = models.TextField(u'Примечание',max_length=300)

    class Meta():
        verbose_name = u"Готовая продукция"

class Pressure(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    tto = models.CharField(u'Номер ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    concavity = models.FloatField(u'Вогнутость')
    perpendicularity = models.FloatField(u'Перпендикулярность')
    flatness = models.FloatField(u'Плоскностность')
    size = models.CharField(u'Размер',max_length=20)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"На сжатие"

class Flexion(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    tto = models.CharField(u'Номер ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    concavity = models.FloatField(u'Вогнутость')
    perpendicularity = models.FloatField(u'Перпендикулярность')
    flatness = models.FloatField(u'Плоскностность')
    size = models.CharField(u'Размер',max_length=20)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"На изгиб"

class Part(models.Model):
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    tto = models.CommaSeparatedIntegerField(u'Номера телег',max_length=30)
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c)
    cause = models.TextField(u'Причина',max_length=600)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Часть партии"