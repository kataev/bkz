# -*- coding: utf-8 -*-
import re
from scipy.lib.blas import get_blas_funcs

from django.core.validators import RegexValidator
from django.utils import datetime_safe as datetime
from django.db import models

from bkz.whs.constants import get_name, get_full_name ,defect_c, color_c, view_c, ctype_c, mark_c, css_dict,cavitation_c
from bkz.utils import UrlMixin,ru_date
from bkz.lab.utils import convert_tto


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

frostresistance_c = (
    (25,u'F25'),
    (35,u'F35'),
    (50,u'F50'),
    (75,u'F75'),
    (100,u'F100'),    
    )


class FrostResistance(models.Model,UrlMixin):
    date = models.DateField(u'Дата', default=datetime.date.today())
    width = models.FloatField(u'Вид кирпича',max_length=30,choices=width_c,default=width_c[0][0])
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c[:-1])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    value = models.IntegerField(u'Значение',choices=frostresistance_c)
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

    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    view = models.CharField(u"Вид кирпича", max_length=60, choices=view_c, default=view_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=ctype_c, default=ctype_c[0][0],blank=True)
    width = models.FloatField(u'Толщина',max_length=30,choices=width_c,default=width_c[0][0])

    heatconduction = models.ForeignKey(HeatConduction,verbose_name=u'Теплопроводность', null=True, blank=True)
    seonr = models.ForeignKey(SEONR,verbose_name=u'Уд.эф.акт.ест.рад.', null=True, blank=True)
    frost_resistance = models.ForeignKey(FrostResistance, verbose_name=u'Морозостойкость', null=True, blank=True)
    water_absorption = models.ForeignKey(WaterAbsorption, verbose_name=u'Водопоглощение', null=True, blank=True)

    volume = models.ForeignKey(u'lab.Test',null=True,blank=True,related_name='volume')
    density = models.FloatField(u'Класс средней плотности',null=True,blank=True)
    weight = models.FloatField(u'Масса',null=True,blank=True)

    tto = models.CharField(u'№ ТТО',max_length=20,null=True,blank=True)
    amount = models.IntegerField(u'Кол-во',null=True,blank=True)
    pressure = models.FloatField(u'При сжатии',null=True,blank=True)
    flexion = models.FloatField(u'При изгибе',null=True,blank=True)
    mark = models.PositiveIntegerField(u"Марка",choices=mark_c[:-1],null=True,blank=True)
    chamfer = models.IntegerField(u'Фаска',null=True,blank=True)

    pf = models.FloatField(u'Пуст. факт.',null=True,blank=True)
    pct = models.FloatField(u'Пуст. прив. к факт.',null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=300,blank=True,null=True)

    def __unicode__(self):
        if self.pk: return u'Партия № %d, %dг' % (self.number,self.date.year)
        else: return u'Новая партия'

    @property
    def get_tto(self):
        return sorted(set(convert_tto(self.tto)))

    @property
    def css(self):
        return css_dict['color'].get(self.color,'None')

    get_name = property(get_name)
    get_full_name = property(get_full_name)

    @models.permalink
    def get_tests_url(self):
        return u'lab:Batch-tests', (), {'pk':self.pk}

    class Meta():
        verbose_name = u"Готовая продукция"
        verbose_name_plural = u"Готовая продукция"
        ordering = ('-date','-number',)

    def get_density_display(self):
        if self.density == 0.8:
            return u'высоко-эффективный'
        elif self.density == 1.0:
            return u'повышенной эффективности'
        elif self.density == 1.4:
            return u'условно-эффективный'
        elif self.density == 2.0:
            return u'малоэффективный (обыкновенный)'



class Cause(models.Model):
    name = models.CharField(u'Имя',max_length=30)
    type = models.CharField(u'тип',max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.type,self.name)
    class Meta:
        ordering = ('type',)

defect_c += ((u'no_cont',u'Некондиция'),)
class Part(models.Model):
    batch = models.ForeignKey(Batch,verbose_name=u'Партия')
    defect = models.CharField(u"Тип", max_length=60, choices=defect_c, blank=False)
    dnumber = models.FloatField(u'Брак.число',default=0)
    half = models.FloatField(u'Половняк',default=3.0)
    cause = models.ManyToManyField('lab.Cause',verbose_name=u'Причина брака',null=True,blank=True)
    limestone = RangeField(u'№ телег c изв.вкл меньше 1см',max_length=30,null=True,blank=True)
    info = models.TextField(u'Примечание',max_length=3000,null=True,blank=True)
    brick = models.ForeignKey('whs.Brick',verbose_name=u'Кирпич',null=True,blank=True)

    def __unicode__(self):
        if self.pk: return u'%s, %s - %d' % (self.get_defect_display(),self.tto,self.amount)
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
    def tto(self):
        s = ''
        if self.defect == u'gost':
            s = ', '
        elif self.defect == u'<20':
            s = '<, '
        elif self.defect == u'>20':
            s = '>, '
        elif self.defect == u'no_cont':
            s = '*, '
        return s.join([r.tto for r in self.rows.all()]) + s

    @property
    def get_limestone_tto(self):
        return convert_tto(self.limestone)

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
    def get_name(self):
        if not self.batch.color:
            return self.batch.get_width_display()
        else:
            return u'%s %s' % (self.batch.get_width_display(),self.batch.get_color_display())

    class Meta():
        verbose_name = u"Часть партии"
        verbose_name_plural = u"Часть партии"
        ordering = ('batch__date','batch__number','defect')


class RowPart(models.Model):
    part = models.ForeignKey(Part,related_name='rows')
    tto = RangeField(u'№ телег',max_length=30)
    amount = models.IntegerField(u'Кол-во')
    test = models.IntegerField(u'Расход на исп',default=0)
    brocken = models.IntegerField(u'Бой',default=0)

    @property
    def out(self):
        return (self.amount or 0) - (self.test or 0) - (self.brocken or 0)

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
        return u'Испытания'