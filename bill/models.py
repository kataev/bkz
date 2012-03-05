# -*- coding: utf-8 -*-
import datetime

from django.db import models

from whs.brick.models import *
from whs.agent.models import Agent
from whs.managers import *




class Oper(models.Model):
    """ Абстрактный класс для всех операций """
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta:
        abstract = True

bill_type_c = (('pickup', 'Самовывоз'), (''))

## Накладная
class Bill(models.Model):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель', related_name="%(app_label)s_%(class)s_related")
    seller = models.ForeignKey(Agent, verbose_name=u'Продавец', related_name="proxy_%(app_label)s_%(class)s_related",
        limit_choices_to={'pk__in': (1, 350)}, help_text=u'', default=350)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    reason = models.CharField(u'Основание', max_length=300, blank=True,
        help_text=u'Основание для выставления товарной накладной')
    type = models.CharField(u'Вид операции', max_length=300, blank=True, help_text=u'')

    class Meta():
        verbose_name = u"Накладная"
        verbose_name_plural = u"Накладные"
        ordering = ['-date', '-number']

    current = CurrendMonthDateDocManager()
    objects = models.Manager()

    def opers(self):
        return list(self.bill_sold_related.all()) + list(self.bill_transfer_related.all())

    @property
    def total(self):
        total = self.bill_sold_related.aggregate(models.Sum('amount'))['amount__sum']
        return total + self.bill_transfer_related.aggregate(models.Sum('amount'))['amount__sum']

    @property
    def tara(self):
        tara = self.bill_sold_related.aggregate(models.Sum('amount'))['amount__sum']
        return tara + self.bill_transfer_related.aggregate(models.Sum('amount'))['amount__sum']

    @property
    def money(self):
        money = self.bill_transfer_related.extra(select={'money':'Sum("amount" * "price")'}).values('money')['money']
        return money + self.bill_sold_related.extra(select={'money':'Sum("amount" * "price")'}).values('money')['money']

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name, self.id)

    def __unicode__(self):
        if self.pk:
            return u'№ %d, %d' % (self.number, self.date.year)
        else:
            return u'Новая накладная'


class Sold(Oper):
    """ Класс для операций отгруки, является аналогом строки в накладной.
Сообщяет нам какой,сколько и по какой цене отгружает кирпич в накладной. """
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    doc = models.ForeignKey(Bill, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Накладная')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
    delivery = models.FloatField(u"Цена доставки", blank=True, null=True, help_text=u'0 если доставки нет')


    class Meta():
        verbose_name = u"Отгрузка"
        verbose_name_plural = u"Отгрузки"
    current = CurrendMonthDateManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Новая отгрузка'

    @property
    def places(self):
        return self.poddon * self.tara

    @property
    def money(self):
        return self.amount * self.price


class Transfer(Oper):
    """ Класс для операций перевода, представляет себя логическую операцию по продажи одной марки
    по цене другой, аналог скидки.
    Содержит только информацию о кол-ве и том кирпиче из которго совершается перевод, конечная
    точка перевода содержится по связи sold.
    Привязанн к накладной, т.к является операцией продажи. """
    brick_from = models.ForeignKey(Brick, related_name="brick_from_%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич откуда", help_text=u'Выберите кирпич')
    brick_to = models.ForeignKey(Brick, related_name="brick_to_%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич куда",
        help_text=u'Выберите кирпич')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
    delivery = models.FloatField(u"Цена доставки", blank=True, null=True, help_text=u'0 если доставки нет')
    doc = models.ForeignKey(Bill, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Накладная')

    @property
    def places(self):
        return self.poddon * self.tara

    @property
    def money(self):
        return self.amount * self.price

    class Meta():
        verbose_name = u"Перевод"
        verbose_name_plural = u"Переводы"
    current = CurrendMonthDateManager()
    objects = models.Manager()

    def __unicode__(self):
        if self.pk:
            return u'Из %s в %s, %d шт' % (self.brick_from,self.brick_to,self.amount)
        else:
            return u'Новый перевод'


