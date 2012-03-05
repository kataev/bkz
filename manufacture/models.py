# -*- coding: utf-8 -*-
from django.db import models

import pytils

from whs.brick.models import *
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
            return u'%s' % date
        else:
            return u'Новая партия с производства'

    @property
    def total(self):
        return sum([x['amount'] for a in self.manufacture_add_related.values('amount').all()])

class Add(models.Model):
    """Класс операций для документа"""
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
            verbose_name = u"Партия"
            verbose_name_plural = u"Партия"

    current = CurrendMonthDateManager()
    objects = models.Manager()
    def __unicode__(self):
        if self.pk:
            return u'%s, %d шт' % (self.brick,self.amount)
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
            return u'от %s %s, %d шт' % (self.date,self.brick,self.amount)
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
            return u'%s, %d шт' % (self.brick,self.amount)
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
            return u'%s, %d шт' % (self.brick,self.amount)
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
            return u'от %s' % self.date
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
            return u'%s, %d шт' % (self.brick,self.amount)
        else:
            return u'Списание'