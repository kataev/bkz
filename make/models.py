# -*- coding: utf-8 -*-
import datetime

from django.db import models

from bkz.utils import UrlMixin,ru_date
from bkz.whs.constants import cavitation_c,color_c,get_name

class Forming(models.Model,UrlMixin):
    """
    Хранит в себе информацию о формовании продукции. Отражается на журнал оператора пресса.
    """
    date = models.DateField(u'Дата', default=datetime.date.today())    
    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])

    tts = models.IntegerField(u'№ ТТС')
    density = models.FloatField(u'Плот.')
    vacuum = models.FloatField(u'Вак.')
    temperature = models.IntegerField(u'Темп.',null=True,blank=True)
    size = models.CharField(u'Размеры, мм',max_length=20,null=True,blank=True)
    humidity = models.FloatField(u'Влаж.',null=True,blank=True)
    conveyor = models.FloatField(u'Kонв.',null=True,blank=True)
    sand = models.FloatField(u'Песок',null=True,blank=True)
    stratcher = models.CommaSeparatedIntegerField(u'Ложок',max_length=300,null=True,blank=True)
    poke = models.CommaSeparatedIntegerField(u'Тычок',max_length=300,null=True,blank=True)
    

    get_name = property(get_name)
    def __unicode__(self):
        if self.pk:
            return u'Формовка %s от %s' % (self.get_name,ru_date(self.date))
        else:
            return u'Новая формовка'
    @property
    def lab(self):
        return list(self.half.all()) + list(self.raw.all()) + list(self.bar.all())

    class Meta:
        verbose_name=u'Формовка'
        verbose_name_plural=u'Формовка'
        unique_together = ('date','tts')
        ordering = ('date',)


class Warren(models.Model,UrlMixin):
    """
    Хранит в себе информацию о садке продукции с сушильных телег на обжиговые телеги. Отражается на журнал оператора садочного коплекса
    """
    date = models.DateField(u'Дата', default=datetime.date.today(),null=True,blank=True)    
    number = models.CharField(u'ТТС',max_length=5)
    path = models.IntegerField(u'Путь',null=True,blank=True)
    source = models.ForeignKey('self',verbose_name=u'ТТС',related_name='consumer',null=True,blank=True)
    brocken = models.IntegerField(u'% брака',default=0)
    cause = models.ManyToManyField('lab.Cause',verbose_name=u'<attr title="Причина брака">П.Б.</attr>',null=True,blank=True,limit_choices_to = {'type':'warren'})

    forming = models.ForeignKey(Forming,verbose_name=u'Формовка',null=True,blank=True,related_name='warrens')
    part = models.ForeignKey('lab.Part',verbose_name=u'Партия',null=True,blank=True,related_name='warrens')

    @property
    def tts(self):
        if self.source:
            return ','.join(self.consumer.all().values_list('number'))
        else:
            return self.number

    @property
    def tto(self):
        if self.source:
            return self.number
        else:
            return self.source.number
            

    def __unicode__(self):
        if self.pk:
            return u'Садка от %s, c ТТC № %s ' % (ru_date(self.date),self.number)
        else:
            return u'Новая садка'

    class Meta:
        ordering = ('-date',)
        verbose_name=u'Садка'
        verbose_name_plural=u'Садка'

