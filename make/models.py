# -*- coding: utf-8 -*-
import datetime

from django.db import models

from bkz.utils import UrlMixin,ru_date
from bkz.whs.constants import cavitation_c,color_c,get_name




class Forming(models.Model,UrlMixin):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today())    
    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер',default=1)
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])

    size = models.CharField(u'Размеры, мм',max_length=20)
    temperature = models.FloatField(u'Темп.')
    humidity = models.FloatField(u'Влаж.')
    vacuum = models.FloatField(u'Вакуум')

    get_name = property(get_name)
    def __unicode__(self):
        if self.pk:
            return u'Формовка %s от %s' % (self.get_name,ru_date(self.date))
        else:
            return u'Новая формовка'

    class Meta:
        verbose_name=u'Формовка'
        verbose_name_plural=u'Формовка'

class TTS(models.Model):
    number = models.IntegerField(u'ТТС')
    forming = models.ForeignKey(Forming,verbose_name=u'Формовка',null=True,blank=True,related_name='tts')

class Warren(models.Model,UrlMixin):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today(),null=True,blank=True)    
    number = models.IntegerField(u'ТТС')
    source = models.ForeignKey('self',verbose_name=u'ТТС',related_name='consumer',null=True,blank=True)
    amount = models.CharField(u'Кол-во',max_length=20)
    tts = models.ForeignKey(TTS,verbose_name=u'Формовка',null=True,blank=True,related_name='warrens')
    part = models.ForeignKey('lab.Part',verbose_name=u'Партия',null=True,blank=True,related_name='warrens')

    def __unicode__(self):
        if self.pk:
            return u'Садка от %s, c ТТC № %d ' % (ru_date(self.date),self.number)
        else:
            return u'Новая садка'

    class Meta:
        ordering = ('-date',)
        verbose_name=u'Садка'
        verbose_name_plural=u'Садка'

