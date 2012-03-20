# -*- coding: utf-8 -*-
from django.db import models
from whs.agent.models import Agent

class Nomenclature(models.Model):
    title = models.CharField(u"Наименование", max_length=200,blank=False,unique=True)
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)

    def __unicode__(self):
        return u'%s - %s' % (self.code,self.title)

class BuxAgent(Agent):
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)