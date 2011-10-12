# -*- coding: utf-8 -*-
from whs.bill.models import Oper,Doc
from django.db import models
from django.contrib import admin
import pytils


class Man(Doc):
    """Класс документа для учета прихода кирпича с производства"""
    class Meta():
            verbose_name = u"производство за день"
            verbose_name_plural = u"производство за день"
    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'Принятие на склад от %s' % date
        else:
            return u'Новый приход'


class Add(Oper):
    """Класс операций для документа"""
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
            verbose_name = u"производство"
            verbose_name_plural = u"производство"
    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc.date)
            return u'Операция принятия на склад от %s' % date
        else:
            return u'Новая операция'

