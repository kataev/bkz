# -*- coding: utf-8 -*-
import pytils
import datetime

from django.core.urlresolvers import reverse

from bkz.brick.models import *


class Man(models.Model):
    """Класс документа для учета прихода кирпича с производства"""
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today(),unique=True)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
        verbose_name = u"Производство"
        verbose_name_plural = u"Производства"
        permissions = (("view_man", u"Может просматривать производсво"),)
        ordering = ('-date', )

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'%s' % date
        else:
            return u'Новая партия с производства'

    def get_absolute_url(self):
        return reverse('man:Man-view',kwargs=dict(pk=self.pk))

class Add(models.Model):
    """Класс операций для документа"""
    brick = models.ForeignKey(Brick, related_name="man", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Man, blank=False, related_name="add", null=False)

    class Meta():
        verbose_name = u"Партия"
        verbose_name_plural = u"Партия"
        ordering = ('-doc__date', )

    def __unicode__(self):
        if self.pk:

            return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Новая партия'

class Sorting(models.Model):
    """ Класс документа для учета перебора кипича из одного товара в другой """
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    brick = models.ForeignKey(Brick, related_name="sorting", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')

    class Meta():
        verbose_name = u"Из цеха"
        permissions = (("view_man", u"Может просматривать операции из цеха"),)

    def get_absolute_url(self):
        return reverse('man:Sort-view',kwargs=dict(pk=self.pk))

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'%s от %s' % (self.brick,date)
        else:
            return u'Новая сортировка'

sorting_c = ((0,u'Отсортированно'),(1,u'Списанно'))

class Sorted(models.Model):
    """ Кирпич после сортировки """
    type = models.IntegerField(u'Тип',choices=sorting_c,help_text=u'Выберите кирпич после сортировки')
    brick = models.ForeignKey(Brick, related_name="sorted",
        verbose_name=u"Кирпич", help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today(),unique=True)
    doc = models.ForeignKey(Sorting, blank=False, related_name="sorted", null=False)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
        verbose_name = u"Сортированый кирпич"
        verbose_name_plural = u"Кирпич после сортировки"

    def __unicode__(self):
        if self.pk:
            return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Новый сортированый кирпич'




class Inventory(models.Model):
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
        verbose_name = u"Инвентаризация"
        verbose_name_plural = u"Инвентаризации"
        permissions = (("view_inventory", u"Может просматривать инвентаризацию"),)

    def get_absolute_url(self):
        return reverse('man:Inventory-view',kwargs=dict(pk=self.pk))

    def __unicode__(self):
        if self.pk:
            return u'от %s' % self.date
        else:
            return u'Новая инвентаризация'


class Write_off(models.Model):
    brick = models.ForeignKey(Brick, related_name="write_off", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Inventory, blank=False, related_name="write_off", null=False)

    class Meta():
        verbose_name = u"Списанние"
        verbose_name_plural = u"Списания"

    def __unicode__(self):
        if self.pk:
            return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Списание'