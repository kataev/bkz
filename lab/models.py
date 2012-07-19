# -*- coding: utf-8 -*-
import re

from django.core.validators import RegexValidator
from django.utils import datetime_safe as datetime
from django.db import models

from bkz.whs.constants import defect_c,color_c,mark_c
from bkz.utils import UrlMixin

slash_separated_float_list_re = re.compile('^([-+]?\d*\.|,?\d+[/\s]*)+$')
validate_slash_separated_float_list = RegexValidator(slash_separated_float_list_re,u'Вводите числа разеделённые дробью','invalid')

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

from south.modelsinspector import add_introspection_rules
add_introspection_rules([],["^bkz\.lab\.models\.SlashSeparatedFloatField"])

class Clay(models.Model,UrlMixin):
    datetime = models.DateTimeField(u'Дата', default=datetime.datetime.now())
    humidity = SlashSeparatedFloatField(u'Пробы влажности',max_length=300)
    sand = models.FloatField(u'Песок %')
    inclusion = models.FloatField(u'Включения %')
    dust = models.FloatField(u'Пылеватость %')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    @property
    def value(self):
        if self.humidity:
            val = [float(v) for v in self.humidity.replace(',','.').split('/') if v]
            return round(sum(val)/len(val),2)
        else:
            return 0

    def __unicode__(self):
        return u'Глина от %s, %.2f' % (self.datetime.date(),self.value)

    class Meta():
        verbose_name = u"Глина"

clay_positions = (
    (1,u'Позиция 1'),
    (2,u'Позиция 2'),
    (3,u'Позиция 3'),
    (4,u'Позиция 4'),
    (5,u'Позиция 5'),
)

class StoredClay(models.Model,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    position = models.IntegerField(u'Позиция',choices=clay_positions,default=1)
    humidity = models.FloatField(u'Влажность')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'Глина от %s, с позиции %.0f %.2f' % (self.datetime.date(),self.position,self.humidity)

    class Meta():
        verbose_name = u"Глина по позициям"

class Sand(models.Model,UrlMixin):
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

class Bar(models.Model,UrlMixin):
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

class Raw(models.Model,UrlMixin):
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
    width = models.FloatField(u'Вид бруса',choices=width_c)
    size = models.CharField(u'Размер',max_length=20)
    weight = models.FloatField(u'Масса')
    humidity = models.FloatField(u'Влажность')
    shrink = models.FloatField(u'Усадка')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Полуфабрикат"

class WaterAbsorption(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'%.2f от %s для %s %s' % (self.value,self.date,self.get_width_display(),self.get_color_display())

    class Meta():
        verbose_name = u"Водопоглащение"

class Efflorescence(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.IntegerField(u'Цвет',choices=color_c)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'от %s для %s' % (self.date,self.get_color_display())

    class Meta():
        verbose_name = u"Высолы"

class FrostResistance(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'%.2f от %s для %s %s' % (self.value,self.date,self.get_width_display(),self.get_color_display())

    class Meta():
        verbose_name = u"Морозостойкость"

class Density(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'%.2f от %s для %s %s' % (self.value,self.date,self.get_width_display(),self.get_color_display())

    class Meta():
        verbose_name = u"Плотность"

class SEONR(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    value = models.FloatField(u'Значение')
    delta = models.FloatField(u'Плюс-минус')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Уд.эф.акт.ест.рад."

class HeatConduction(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Теплопроводность"


class Batch(UrlMixin,models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ партии')
    tto = models.CharField(u'Номер ТТО',max_length=20)
    amount = models.IntegerField(u'Кол-во')
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c)
    color = models.IntegerField(u'Цвет',choices=color_c)
    water_absorption = models.ForeignKey(WaterAbsorption, verbose_name=u'Водопоглощение', null=True, blank=True)
    efflorescence = models.ForeignKey(Efflorescence, verbose_name=u'Высолы', null=True, blank=True)
    frost_resistance = models.ForeignKey(FrostResistance, verbose_name=u'Морозостойкость', null=True, blank=True)
    density = models.ForeignKey(Density,verbose_name=u'Плотность')
    seonr = models.ForeignKey(SEONR,verbose_name=u'Уд.эф.акт.ест.рад.')
    heatconduction = models.ForeignKey(HeatConduction,verbose_name=u'Теплопроводность')
    inclusion = models.TextField(u'Включения',null=True,blank=True)
    pressure = models.FloatField(u'При сжатии')
    flexion = models.FloatField(u'При изгибе')
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c)
    chamfer = models.IntegerField(u'Фаска')
    info = models.TextField(u'Примечание',max_length=300,blank=True,null=True)

    def __unicode__(self):
        if self.pk: return u'Партия № %d, %d г.' % (self.number,self.date.year)
        else: return u'Новая партия'

    class Meta():
        verbose_name = u"Готовая продукция"
        verbose_name_plural = u"Готовая продукция"

class Pressure(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name=u'pressure_tests')
    tto = models.CharField(u'Номер ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    concavity = models.FloatField(u'Вогнутость')
    perpendicularity = models.FloatField(u'Перпендикулярность')
    flatness = models.FloatField(u'Плоскностность')
    size = models.CharField(u'Размер',max_length=20)
    value = models.FloatField(u'Значение')

    def __unicode__(self):
        if self.pk: return u'Испытания на сжатие партии № %d, %d г.' % (self.batch.number,self.batch.date.year)
        else: return u'Новое испытание'


    class Meta():
        verbose_name = u"На сжатие"
        verbose_name_plural = u"На сжатие"

class Flexion(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name=u'flexion_tests')
    tto = models.CharField(u'Номер ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    concavity = models.FloatField(u'Вогнутость')
    perpendicularity = models.FloatField(u'Перпендикулярность')
    flatness = models.FloatField(u'Плоскностность')
    size = models.CharField(u'Размер',max_length=20)
    value = models.FloatField(u'Значение')

    class Meta():
        verbose_name = u"На изгиб"
        verbose_name_plural = u"На изгиб"

class Part(models.Model):
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    tto = models.CommaSeparatedIntegerField(u'Номера телег',max_length=30)
    amount = models.IntegerField(u'Кол-во')
    test = models.IntegerField(u'Расход кирпича на испытание')
    half = models.FloatField(u'Половняк')
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c)
    dnumber = models.FloatField(u'Браковочное число')
    cause = models.TextField(u'Причина',max_length=600)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    class Meta():
        verbose_name = u"Часть партии"
        verbose_name_plural = u"Часть партии"