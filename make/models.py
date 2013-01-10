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
    tts = models.CharField(u'№ ТТС',max_length=200,help_text=u'Перечислите номера ТТС через запятую')

    get_name = property(get_name)
    def __unicode__(self):
        if self.pk:
            return u'Формовка %s от %s, %s' % (self.get_name,ru_date(self.date),self.tts)
        else:
            return u'Новая формовка'

    class Meta:
        verbose_name=u'Формовка'
        verbose_name_plural=u'Формовка'

class Warren(models.Model,UrlMixin):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today(),null=True,blank=True)    
    number = models.IntegerField(u'ТТС')
    source = models.ForeignKey('self',verbose_name=u'ТТС',related_name='consumer',null=True,blank=True)
    amount = models.CharField(u'Кол-во',max_length=20)

    def __unicode__(self):
        if self.pk:
            return u''  
            if self.source:
                return u'Садка от %s, c ТТC № %d ' % (ru_date(self.date),self.number)
            else:
                return u'Садка от %s, на ТТО № %d' % (ru_date(self.date),self.number)
        else:
            return u'Новая садка'

    class Meta:
        ordering = ('-date',)
        verbose_name=u'Садка'
        verbose_name_plural=u'Садка'