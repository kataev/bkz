# -*- coding: utf-8 -*-
from django.db import models

import pytils
import datetime

from whs.bill.models import *
from whs.brick.models import Brick
from whs.managers import *

class Man(models.Model):
    """Класс документа для учета прихода кирпича с производства"""
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
            verbose_name = u"Производство"
            verbose_name_plural = u"Производства"

    current = CurrendMonthDateDocManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'Принятие на склад от %s' % date
        else:
            return u'Новая партия с производства'

    @property
    def total(self):
        return sum([x['amount'] for a in self.manufacture_add_related.values('amount').all()])

class Add(Oper):
    """Класс операций для документа"""
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
            verbose_name = u"Партия"
            verbose_name_plural = u"Партия"

    current = CurrendMonthDateManager()
    objects = models.Manager()
    def __unicode__(self):
        if self.pk:
            return u'Партия %s' % self.brick
        else:
            return u'Новая партия'


class Sorting(models.Model):
    """ Класс документа для учета перебора кипича из одного товара в другой """
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    class Meta():
        verbose_name = u"Сортировка"
        verbose_name_plural = u"Сортировки"

    current = CurrendMonthDateDocManager()
    objects = models.Manager()

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name, self.id)

    def __unicode__(self):
        if self.pk:
            return u'Сортировка от %s' % self.date
        else:
            return u'Новая сортировка'


class Sorted(models.Model):
    """ Кирпич принятый из сортировки """
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич", help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Sorting,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
        verbose_name = u"Сортированый кирпич"
        verbose_name_plural = u"Кирпич после сортировки"
    current = CurrendMonthDateManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'После сортировки %s' % self.brick
        else:
            return u'Новый сортированый кирпич'

class Removed(models.Model):
    """ Списание при сортировке """
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Sorting,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
        verbose_name = u"Списанный кирпич"
        verbose_name_plural = u"Списанные"
    current = CurrendMonthDateManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'Списаный %s' % self.brick
        else:
            return u'Списание'

class Inventory(models.Model):
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
        verbose_name = u"Инвентаризация"
        verbose_name_plural = u"Инвентаризации"
    current = CurrendMonthDateDocManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'Инвентаризация от %s' % self.date
        else:
            return u'Новая инвентаризация'

class Write_off(models.Model):
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Inventory,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
        verbose_name = u"Списанние"
        verbose_name_plural = u"Списания"
    current = CurrendMonthDateManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'Списаный %s' % self.brick
        else:
            return u'Списание'