# -*- coding: utf-8 -*-
import datetime

from django.db import models

from bkz.whs.constants import cavitation_c,view_c,color_c

class Forming(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today())    
    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    view = models.CharField(u"Вид кирпича", max_length=60, choices=view_c, default=view_c[0][0])
    color = models.IntegerField(u'Цвет',choices=color_c,default=color_c[0][0])
    tts = models.CharField(u'ТТС',max_length=200)

class WarrenTTS(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today())    
    tts = models.CharField(u'ТТС',max_length=20)

class WarrenTTO(models.Model):
    timestamp = models.DateTimeField(u'Время создания',auto_now=True,)
    date = models.DateField(u'Дата', default=datetime.date.today())    
    tto = models.CharField(u'№ ТТО',max_length=20)
    tts = models.ForeignKey(WarrenTTS,verbose_name=u'ТТС',related_name='tto')