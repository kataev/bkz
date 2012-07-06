# -*- coding: utf-8 -*-
from django.utils import datetime_safe as datetime
from django.db import models

from whs.brick.constants import mark_c,defect_c,color_c

class Clay(models.Model):
    datetime = models.DateTimeField(u'Дата', default=datetime.time.now())
    humidity = models.CommaSeparatedIntegerField(u'Пробы влажности',max_length=300)
    sand = models.FloatField(u'Песок %')
    inclusion = models.FloatField(u'Включения %')
    dust = models.FloatField(u'Пылеватость %')
    info = models.TextField(u'Примечание',max_length=3000)

    class Meta():
        verbose_name = u"Глина из карьера"

class StoredClay(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.time.now())
    position = models.TextField(u'Позиция',max_length=300)
    humidity = models.FloatField(u'Влажность')

    class Meta():
        verbose_name = u"Глина по позициям"

class Sand(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    humidity = models.FloatField(u'Влажность')
    particle_size = models.FloatField(u'Гранулометричский состав')
    module_size = models.FloatField(u'Модуль крупности')
    dirt = models.TextField(u'Включения')
    info = models.TextField(u'Примечание',max_length=3000)

    class Meta():
        verbose_name = u"Песок"

class Bar(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.time.now())
    width = models.CharField(u'Вид бруса')
    tts = models.CharField(u'Номер ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    temperature = models.FloatField(u'Температура')
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    sand = models.FloatField(u'Влажность')
    poke_left = models.CommaSeparatedIntegerField(u'Тычок левый',max_length=300)
    poke_right = models.CommaSeparatedIntegerField(u'Тычок правый',max_length=300)
    stratcher_left = models.CommaSeparatedIntegerField(u'Ложок левый',max_length=300)
    stratcher_right = models.CommaSeparatedIntegerField(u'Ложок правый',max_length=300)
    humidity_transporter = models.FloatField(u'Влажность с конвейера')
    info = models.TextField(u'Примечание',max_length=3000)

    class Meta():
        verbose_name = u"Брус"

class Raw(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.time.now())
    tts = models.CharField(u'Номер ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    temperature = models.FloatField(u'Температура')
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    info = models.TextField(u'Примечание',max_length=3000)

    class Meta():
        verbose_name = u"Сырец из накопителя"

class Half(models.Model):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.time.now())
    position = models.IntegerField(u'Позиция')
    path = models.IntegerField(u'Путь')
    width = models.CharField(u'Вид бруса',max_length=30)
    size = models.CharField(u'Размер',max_length=20)
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    shrink = models.FloatField(u'Усадка')

    class Meta():
        verbose_name = u"Полуфабрикат"

class WaterAbsorption(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30,choices=color_c)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"Водопоглащение"

class Efflorescence(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"Высолы"

class FrostResistance(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"Морозостойкость"

class Density(models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.CharField(u'Вид кирпича',max_length=30)
    color = models.CharField(u'Цвет',max_length=30)
    value = models.FloatField(u'Значение')

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
    tto = models.CommaSeparatedIntegerField(u'Номера телег')
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c)
    cause = models.TextField(u'Причина',max_length=600)

    class Meta():
        verbose_name = u"Часть партии"