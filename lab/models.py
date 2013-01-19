# -*- coding: utf-8 -*-
import re
import datetime

from django.core.validators import RegexValidator
from django.db import models

from bkz.whs.constants import *
from bkz.utils import UrlMixin,ru_date
from bkz.lab.utils import convert_tto,ShiftMixin
from bkz.make.models import Warren,Forming,TTS

slash_separated_float_list_re = re.compile('^([-+]?\d*\.|,?\d+[/\s]*)+$')
validate_slash_separated_float_list = RegexValidator(slash_separated_float_list_re,u'Вводите числа разеделённые дробью','invalid')

class SlashSeparatedFloatField(models.CharField):
    default_validators = [validate_slash_separated_float_list]
    description = u'Slash-separated floats'

    def formfield(self,**kwargs):
        defaults = {'error_messages': {'invalid': u'Вводите числа разеделённые косой чертой (/)'} } 
        defaults.update(kwargs)
        return super(SlashSeparatedFloatField,self).formfield(**defaults)

range_list_re = re.compile('^[\d,-]+$')

validate_range_list = RegexValidator(range_list_re,u'Вводите числа разеделённые дробью','invalid')

class RangeField(models.CharField):
    default_validators = [validate_range_list]
    description = u'Range field'

    def formfield(self,**kwargs):
        defaults = {'error_messages': {'invalid': u'Вводите числа разеделённые дробью'} }
        defaults.update(kwargs)
        return super(RangeField,self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([],["^bkz\.lab\.models\.SlashSeparatedFloatField","^bkz\.lab\.models\.RangeField"])

class Clay(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    humidity = models.FloatField(u'Влаж.')
    sand = models.FloatField(u'Песок',null=True,blank=True)
    inclusion = models.FloatField(u'Включ.',null=True,blank=True)
    dust = models.FloatField(u'Пылев.',null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    @property
    def value(self):
        if self.humidity:
            try: val = [float(v) for v in self.humidity.replace(',','.').split('/') if v]
            except BaseException: return None
            return round(sum(val)/len(val),2)
        else:
            return 0

    def __unicode__(self):
        if self.pk: return u'Проба глины от %s %s' % (ru_date(self.datetime.date()),self.datetime.time())
        else: return u'Новая проба глины из карьера'

    class Meta():
        verbose_name = u"Глина"
        verbose_name_plural = u"Глины"
        ordering = ('datetime',)

clay_positions = (
    (1,u'1 позиция'),
    (2,u'2 позиция'),
    (3,u'3 позиция'),
    (4,u'4 позиция'),
    (5,u'5 позиция'),
    (6,u'Белая глина'),
)

class StoredClay(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    position = models.IntegerField(u'Позиция',choices=clay_positions,default=1)
    used = models.BooleanField(u'<abbr title="По этой позиции формовали?">Ф</abbr>',default=False)
    humidity = models.FloatField(u'Влаж.')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'Глина от %s, с позиции %.0f %.2f' % (ru_date(self.datetime.date()),self.position,self.humidity)
        else: return u'Новая проба глины со склада'

    class Meta():
        verbose_name = u"Глина по позициям"
        verbose_name_plural = u"Глины по позициям"
        ordering = ('datetime','-position')

class Sand(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    humidity = models.FloatField(u'Влаж.')
    particle_size = models.FloatField(u'<abbr title=Гран. состав>ГС</abbr>',null=True,blank=True)
    module_size = models.FloatField(u'<abbr title="Модуль крупности">МК</abbr>',null=True, blank=True)
    dirt = models.TextField(u'Включения',null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'Проба песка от %s' % ru_date(self.datetime)
        else: return u'Новая проба песка'

    class Meta:
        verbose_name = u"Песок"
        verbose_name_plural = u"Песка"
        ordering = ('datetime',)


width_c = (
    (0.8,u'Евро'),
    (1.0,u'Одинарный'),
    (1.4,u'Утолщенный'),
)

class Bar(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    cavitation = models.IntegerField(u"Пустот.", choices=cavitation_c, default=0)
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)

    tts = models.CharField(u'ТТС',max_length=20)
    size = models.CharField(u'Размеры, мм',max_length=20)
    humidity = models.FloatField(u'Влаж.')
    weight = models.FloatField(u'Масса')
    temperature = models.FloatField(u'Темп.')
    sand = models.FloatField(u'Песок')
    humidity_transporter = models.FloatField(u'<abbr title="Влажность с конвейера, %">ВсК</abbr>',null=True)

    poke_left = models.CommaSeparatedIntegerField(u'Тычок левый',max_length=300)
    poke_right = models.CommaSeparatedIntegerField(u'Тычок правый',max_length=300)
    stratcher_left = models.CommaSeparatedIntegerField(u'Ложок левый',max_length=300)
    stratcher_right = models.CommaSeparatedIntegerField(u'Ложок правый',max_length=300)
    cutter = models.CommaSeparatedIntegerField(u'Отрезчик',max_length=3000)
    info = models.TextField(u'Примечание',max_length=3000)

    forming = models.ForeignKey(TTS,verbose_name=u'Формовка',null=True,blank=True,related_name='bars')

    def __unicode__(self):
        if self.pk: return u'Брус от %s с телеги №%s' % (ru_date(self.datetime),self.tts)
        else: return u'Новый брус'

    class Meta():
        verbose_name = u"Брус"
        verbose_name_plural = u"Бруса"
        ordering = ('datetime',)

class Raw(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())
    cavitation = models.PositiveIntegerField(u"Пустот.", choices=cavitation_c, default=cavitation_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)

    tts = models.CharField(u'ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    humidity = models.FloatField(u'Влаж.')
    weight = models.FloatField(u'Масса')
    temperature = models.FloatField(u'Темп.')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    forming = models.ForeignKey(TTS,verbose_name=u'Формовка',null=True,blank=True,related_name='raws')

    def __unicode__(self):
        if self.pk: return u'Сырец от %s с телеги №%s' % (ru_date(self.datetime),self.tts)
        else: return u'Новый сырец'

    class Meta():
        verbose_name = u"Сырец из накопителя"
        verbose_name_plural = u"Сырца из накопителя"
        ordering = ('datetime',)

class Half(models.Model,ShiftMixin,UrlMixin):
    datetime = models.DateTimeField(u'Дата и время', default=datetime.datetime.now())

    cavitation = models.PositiveIntegerField(u"Пустот.", choices=cavitation_c, default=cavitation_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)

    tts = models.CharField(u'ТТС',max_length=20)
    size = models.CharField(u'Размер',max_length=20)
    humidity = models.FloatField(u'Влаж.')
    weight = models.FloatField(u'Масса')
    shrink = models.FloatField(u'<attr title="Усадка, %">Усдк</attr>')
    path = models.IntegerField(u'Путь')
    position = models.IntegerField(u'Поз.')
    
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    forming = models.ForeignKey(TTS,verbose_name=u'Формовка',null=True,blank=True,related_name='halfs')

    @property
    def css(self):
        return u'path-%d position-%d' % (self.path or 0,self.position or 0)

    def __unicode__(self):
        if self.pk: return u'Полуфабрикат от %s с поз №%d, путь №%d' % (ru_date(self.datetime),self.position,self.path)
        else: return u'Новый полуфабрикат'

    class Meta():
        verbose_name = u"Полуфабрикат"
        verbose_name_plural = u"Полуфабриката"
        ordering = ('datetime','-path','-position')

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
    value = models.IntegerField(u'Значение',choices=frostresistance_c)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk:
            return u'%d от %s для %s %s' % (self.value,ru_date(self.date),self.get_width_display(),self.get_color_display())
        else:
            return u'Новое значение морозостойкости'

    class Meta():
        verbose_name = u"Морозостойкость"

class SEONR(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.FloatField(u'Значение')
    delta = models.FloatField(u'Плюс-минус')
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'%s для %s' % (self.get_name,self.get_color_display())
        else: return u'Новое значение радионуклидов'

    @property
    def get_name(self):
        return u'%.2f\u00b1%.2f' % (self.value or 0,self.delta or 0)

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

    def get_value_display(self):
        if self.value < 0.20:
            return u'Высокой эффективности'
        elif 0.20 < self.value < 0.24:
            return u'Повышенной эффективности'
        elif 0.24 < self.value < 0.36:
            return u'Эффективный'
        elif 0.36 < self.value < 0.46:
            return u'Условно-эффективные'
        elif 0.46 < self.value:
            return u'Малоэффективные'

class Batch(UrlMixin,models.Model):
    date = models.DateField(u'Дата', default=datetime.date.today())
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ партии')

    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    view = models.CharField(u"Вид кирпича", max_length=60, choices=view_c, default=view_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=ctype_c, default='0')
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)

    heatconduction = models.ForeignKey(HeatConduction,verbose_name=u'Теплопроводность', null=True, blank=True)
    seonr = models.ForeignKey(SEONR,verbose_name=u'Уд.эф.акт.ест.рад.', null=True, blank=True)
    frost_resistance = models.ForeignKey(FrostResistance, verbose_name=u'Морозостойкость', null=True, blank=True)
    water_absorption = models.ForeignKey(WaterAbsorption, verbose_name=u'Водопоглощение', null=True, blank=True)

    volume = models.ForeignKey(u'lab.Test',null=True,blank=True,related_name='volume_test')
    cad = models.FloatField(u'Класс средней плотности',null=True,blank=True,choices=cad_c)
    density = models.FloatField(u'Плотность',null=True,blank=True)
    weight = models.FloatField(u'Масса',null=True,blank=True)

    tto = models.CharField(u'№ ТТО',max_length=20,null=True,blank=True)
    amount = models.IntegerField(u'Кол-во',null=True,blank=True)
    pressure = models.FloatField(u'При сжатии',null=True,blank=True)
    flexion = models.FloatField(u'При изгибе',null=True,blank=True)
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c[:-1],null=True,blank=True)
    chamfer = models.IntegerField(u'Фаска',default=3)

    pf = models.FloatField(u'Пустотность фактическая',null=True,blank=True)
    pct = models.FloatField(u'Пустотность приведенная к фактической',null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=300,blank=True,null=True)

    @property
    def get_warren(self):
        tto = self.get_tto
        dr = (self.date - datetime.timedelta(days=5),self.date - datetime.timedelta(days=3))
        return Warren.objects.order_by('-date','number').values_list('number','consumer__number').filter(source__isnull=True).filter(number__in=tto).filter(date__range=dr)

    def __unicode__(self):
        if self.pk: return u'Партия № %d, %dг' % (self.number,self.date.year)
        else: return u'Новая партия'

    @property
    def get_tto(self):
        return sorted(set(convert_tto(self.tto)))

    @property
    def css(self):
        return css_dict['color'].get(self.color,'None')

    @property
    def parts_by_defect(self):
        return map(lambda x:[p for p in self.parts.all() if p.defect==x[0]],defect_c[:-1])

    @property
    def gost(self):
        return sum(map(lambda x:sum([p.out for p in self.parts.all() if p.defect=='gost']),defect_c[:-1]))

    @property
    def l20(self):
        return sum(map(lambda x:sum([p.out for p in self.parts.all() if p.defect=='<20']),defect_c[:-1]))

    @property
    def m20(self):
        return sum(map(lambda x:sum([p.out for p in self.parts.all() if p.defect=='>20']),defect_c[:-1]))


    get_name = property(get_name)
    get_full_name = property(get_full_name)

    @models.permalink
    def get_tests_url(self):
        return u'lab:Batch-tests', (), {'pk':self.pk}

    class Meta():
        verbose_name = u"Готовая продукция"
        verbose_name_plural = u"Готовая продукция"
        ordering = ('-date','-number',)

    @property
    def get_cad_display(self):
        if self.cad == 0.8:
            return u'высоко-эффективный'
        elif self.cad == 1.0:
            return u'повышенной эффективности'
        elif self.cad == 1.4:
            return u'условно-эффективный'
        elif self.cad == 2.0:
            return u'малоэффективный (обыкновенный)'



class Cause(models.Model):
    name = models.CharField(u'Имя',max_length=30)
    type = models.CharField(u'тип',max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.type,self.name)
    class Meta:
        ordering = ('type',)

class Part(models.Model):
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name='parts')
    defect = models.CharField(u"Качество", max_length=60, choices=defect_c, blank=False)
    dnumber = models.FloatField(u'Брак.число',default=0)
    half = models.FloatField(u'Половняк',default=3.0)
    cause = models.ManyToManyField('lab.Cause',verbose_name=u'Причина брака',null=True,blank=True)
    limestone = RangeField(u'№ телег c изв.вкл меньше 1см²',max_length=30,null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)
    brick = models.ForeignKey('whs.Brick',verbose_name=u'Кирпич',null=True,blank=True)

    def __unicode__(self):
        if self.pk: 
            s = u'%s - %d шт, %d' % (self.get_defect_display(),self.amount or 0,len(self.get_tto))
            if self.limestone:
                s+= u'(%d)' % (len(self.get_limestone_tto))
            s+= u' ТТО'
            return s
        else: return u'Новый выход с производства'

    @property
    def get_tto(self):
        return convert_tto(self.tto)

    @property
    def amount(self):
        return sum([r.amount for r in self.rows.all()])

    @property
    def out(self):
        return sum([r.out for r in self.rows.all()])

    @property
    def brocken(self):
        return sum([r.brocken for r in self.rows.all()])

    @property
    def test(self):
        return sum([r.test for r in self.rows.all()])

    @property
    def tto(self):
        if self.defect == u'gost':
            s = '%s'
        elif self.defect == u'<20':
            s = '(%s)'
        elif self.defect == u'>20':
            s = '[%s]'
        else:
            s = '{%s}'
        return s % ','.join([r.tto or '' for r in self.rows.all()])

    @property
    def get_limestone_tto(self):
        if self.limestone: return convert_tto(self.limestone)
        else: return []

    @property
    def get_cause_display(self):
        return ', '.join([p.name for p in self.cause.all()])

    @property
    def get_css_class(self):
        if not self.pk:
            return ''
        if self.defect == u' ':
            return 'success'
        elif self.defect == u'<20':
            return 'info'
        else:
            return 'error'
    @property
    def get_warren_tts(self):
        q =  Warren.objects.order_by('-date','number')\
                                .filter(date__lt=self.batch.date)\
                                .filter(number__in=self.get_tto)[:len(self.get_tto)]
        print q.query
        return q


    class Meta():
        verbose_name = u"Часть партии"
        verbose_name_plural = u"Часть партии"
        ordering = ('-batch__date','-batch__number',)


class RowPart(models.Model):
    part = models.ForeignKey(Part,related_name='rows')
    tto = RangeField(u'№ телег',max_length=30)
    amount = models.IntegerField(u'Кол-во')
    test = models.IntegerField(u'Расход на исп',default=0)
    brocken = models.IntegerField(u'Бой',default=0)

    @property
    def out(self):
        return (self.amount or 0) - (self.test or 0) - (self.brocken or 0)

    @property
    def get_tto(self):
        return convert_tto(self.tto)

test_c = ((u'flexion',u'На изгиб'), (u'pressure',u'На сжатие'),)

class Test(models.Model):
    type = models.CharField(u'Тип',max_length=10,choices=test_c)
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    batch = models.ForeignKey(Batch,verbose_name=u'Партия',related_name=u'tests')
    tto = models.CharField(u'№ ТТО',max_length=20)
    row = models.IntegerField(u'Ряд')
    size = models.CharField(u'Размеры',max_length=20)
    area = models.FloatField(u'S²')
    readings = models.FloatField(u'H')
    value = models.FloatField(u'Знач',default=0.0)

    def __unicode__(self):
        return u'Испытания %s' % self.get_type_display().lower()
    @property
    def volume(self):
        if self.size:
            size = map(float,self.size.split('x'))
            return (size[0] * size[1] * size[2]) / pow(100*10,3)

    class Meta:
        ordering = ('row',)
        verbose_name=u'Испытания'
