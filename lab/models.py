# -*- coding: utf-8 -*-
import re

from django.core.validators import RegexValidator
from django.utils import datetime_safe as datetime
from django.db import models

from bkz.whs.constants import defect_c,color_c,mark_c
from bkz.utils import UrlMixin,ru_date


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

range_list_re = re.compile('^[\d,-]+$')

validate_range_list = RegexValidator(range_list_re,u'Вводите числа разеделённые дробью','invalid')

class RangeField(models.CharField):
    default_validators = [validate_range_list]
    description = u'Range field'

    def formfield(self,**kwargs):
        defaults = {
            'error_messages': {
                'invalid': u'Вводите числа разеделённые дробью'
            }
        }
        defaults.update(kwargs)
        return super(RangeField,self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([],["^bkz\.lab\.models\.SlashSeparatedFloatField","^bkz\.lab\.models\.RangeField"])

class Clay(models.Model,UrlMixin):
    datetime = models.DateTimeField(u'Дата', default=datetime.datetime.now())
    humidity = SlashSeparatedFloatField(u'Пробы влажности',max_length=300)
    sand = models.FloatField(u'Песок')
    inclusion = models.FloatField(u'Включения')
    dust = models.FloatField(u'Пылеватость')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    @property
    def value(self):
        if self.humidity:
            val = [float(v) for v in self.humidity.replace(',','.').split('/') if v]
            return round(sum(val)/len(val),2)
        else:
            return 0

    def __unicode__(self):
        if self.pk: return u'Проба глины от %s %s' % (ru_date(self.datetime.date()),self.datetime.time())
        else: return u'Новая проба глины из карьера'

    class Meta():
        verbose_name = u"Глина"

clay_positions = (
    (1,u'1 позиция'),
    (2,u'2 позиция'),
    (3,u'3 позиция'),
    (4,u'4 позиция'),
    (5,u'5 позиция'),
)

class StoredClay(models.Model,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    position = models.IntegerField(u'Позиция',choices=clay_positions,default=1)
    humidity = models.FloatField(u'Влажность')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'Глина от %s, с позиции %.0f %.2f' % (ru_date(self.datetime.date()),self.position,self.humidity)
        else: return u'Новая проба глины со склада'

    class Meta():
        verbose_name = u"Глина по позициям"

class Sand(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    humidity = models.FloatField(u'Влажность')
    particle_size = models.FloatField(u'Гран. состав')
    module_size = models.FloatField(u'Модуль крупности')
    dirt = models.TextField(u'Включения')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'Проба песка от %s' % ru_date(self.date)
        else: return u'Новая проба песка'

    class Meta():
        verbose_name = u"Песок"


width_c = (
    (0.8,u'Евро'),
    (1.0,u'Одинарный'),
    (1.4,u'Утолщенный'),
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

    def __unicode__(self):
        if self.pk: return u'Брус от %s' % self.datetime
        else: return u'Новый брус'

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

    def __unicode__(self):
        if self.pk: return u'Сырец от %s' % self.datetime
        else: return u'Новый сырец'

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

    def __unicode__(self):
        if self.pk: return u'Полуфабрикат с поз № %d от %s' % (self.humidity,ru_date(self.datetime))
        else: return u'Новый полуфабрикат'

    class Meta():
        verbose_name = u"Полуфабрикат"

class WaterAbsorption(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'%.2f от %s для %s %s' % (self.value,ru_date(self.date),self.get_width_display(),self.get_color_display())
        else: return u'Новая проба водопоглащения'

    class Meta():
        verbose_name = u"Водопоглащение"

class Efflorescence(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'от %s для %s' % (ru_date(self.date),self.get_color_display())
        else: return u'Новая проба высолов'

    class Meta():
        verbose_name = u"Высолы"

class FrostResistance(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c[:-1])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk:
            return u'%.0f от %s для %s %s' % (self.value,ru_date(self.date),self.get_width_display(),self.get_color_display())
        else:
            return u'Новое значение морозостойкости'

    class Meta():
        verbose_name = u"Морозостойкость"

class Density(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        return u'%.2f от %s для %s %s' % (self.value,ru_date(self.date),self.get_width_display(),self.get_color_display())

    class Meta():
        verbose_name = u"Плотность"

class SEONR(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.FloatField(u'Значение')
    delta = models.FloatField(u'Плюс-минус')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'%.2f\u00b1%.2f для %s' % (self.value,self.delta,self.get_color_display())
        else: return u'Новое значение радионуклидов'

    class Meta():
        verbose_name = u"Уд.эф.акт.ест.рад."

class HeatConduction(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    value = models.FloatField(u'Значение')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk:
            return u'%.2f от %s' % (self.value,ru_date(self.date))
        else:
            return u'Новые измерения теплопроводности'

    class Meta():
        verbose_name = u"Теплопроводность"

cavitation = (
    (True,u'Пустотелый'),
    (False,u'Полнотелый')
)


class Batch(UrlMixin,models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ партии')

    cavitation = models.BooleanField(u"Кирпич",default=True)
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])

    heatconduction = models.ForeignKey(HeatConduction,verbose_name=u'Теплопроводность', null=True, blank=True)
    seonr = models.ForeignKey(SEONR,verbose_name=u'Уд.эф.акт.ест.рад.', null=True, blank=True)
    frost_resistance = models.ForeignKey(FrostResistance, verbose_name=u'Морозостойкость', null=True, blank=True)
    water_absorption = models.ForeignKey(WaterAbsorption, verbose_name=u'Водопоглощение', null=True, blank=True)
    density = models.FloatField(u'Класс средней плотности')
    weight = models.FloatField(u'Масса')

    tto = models.CharField(u'№ ТТО',max_length=20,null=True,blank=True)
    amount = models.IntegerField(u'Кол-во',null=True,blank=True)
    pressure = models.FloatField(u'При сжатии',null=True,blank=True)
    flexion = models.FloatField(u'При изгибе',null=True,blank=True)
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c[:-1],default=mark_c[0][0])
    chamfer = models.IntegerField(u'Фаска',null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=300,blank=True,null=True)

    def __unicode__(self):
        if self.pk: return u'Партия № %d, %dг' % (self.number,self.date.year)
        else: return u'Новая партия'

    class Meta():
        verbose_name = u"Готовая продукция"
        verbose_name_plural = u"Готовая продукция"
    def get_density_display(self):
        if self.density > 1.4:
            return u'условно-эффективный'
        else:
            return u'эффективный'

class Pressure(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name=u'pressure_tests')
    tto = models.CharField(u'№ ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    size = models.CharField(u'Размер',max_length=20)
    area = models.FloatField(u'Площадь')
    readings = models.FloatField(u'Показание прибора')
    value = models.FloatField(u'Значение',default=0.0)

    def __unicode__(self):
        if self.pk: return u'Испытания на сжатие партии № %d, %d г.' % (self.batch.number,self.batch.date.year)
        else: return u'Новое испытание'

    class Meta():
        verbose_name = u"Испытание еа сжатие"
        verbose_name_plural = u"Испытания на сжатие"

class Flexion(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name=u'flexion_tests')
    tto = models.CharField(u'№ ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    size = models.CharField(u'Размер',max_length=20)
    area = models.FloatField(u'Площадь')
    readings = models.FloatField(u'Показание прибора')
    value = models.FloatField(u'Значение',default=0.0)

    class Meta():
        verbose_name = u"Испытание на изгиб"
        verbose_name_plural = u"Испытания на изгиб"

cause_c = (
    ('0',u'Бой'),
    ('1',u'Трешины'),
    ('2',u'Извесняк.вкл >`1см²'),
    ('3',u'Другое, указать в примечании'),
    )

class Part(models.Model):
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    tto = RangeField(u'№ телег',max_length=30,blank=True)
    amount = models.IntegerField(u'Кол-во')
    test = models.IntegerField(u'Расход на исп',default=0)
    defect = models.CharField(u"Тип", max_length=60, choices=defect_c,default=defect_c[0][0])
    half = models.FloatField(u'Половняк',default=3)
    dnumber = models.FloatField(u'Брак.число',default=0)
    cause = models.ManyToManyField('whs.Features',verbose_name=u'Причина брака')
    brocken = models.IntegerField(u'Бой',default=0)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)
    sorted = models.BooleanField(u'Сортирован',default=False)

    def __unicode__(self):
        if self.pk: return u'%s, %s c телег %s' % (self.batch,self.get_defect_display().lower(),self.tto)
        else: return u'Новый выход с производства'

    @property
    def get_name(self):
        if not self.batch.color:
            return self.batch.get_width_display()
        else:
            return u'%s %s' % (self.batch.get_width_display(),self.batch.get_color_display())

    @property
    def count_exit(self):
        return self.amount

    class Meta():
        verbose_name = u"Часть партии"
        verbose_name_plural = u"Часть партии"
        ordering = ('batch__date','batch__number','defect')