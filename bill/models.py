# -*- coding: utf-8 -*-
from django.db import models
from whs.brick.models import Brick
from whs.agent.models import Agent
import pytils
import datetime
from django.core.exceptions import ValidationError
from django.db.models import Max

class Oper(models.Model):
    """ Абстрактный класс для всех операций """
    poddon_c = ((288, u'Маленький поддон'), (352, u'Обычный поддон'))

    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    def get_id(self):
        return u'%s.%s__%d' % (self._meta.app_label, self._meta.module_name, self.pk)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/%s/%d/' % (self._meta.module_name.lower(), self.pk)


class Doc(models.Model):
    """ Абстрактный класс для документов. """
    draft_c = ((False, u'Чистовик'), (True, u'Черновик'))
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    draft = models.BooleanField(u'Черновик', default=True, choices=draft_c,
        help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True


## Накладная
class Bill(Doc):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель', related_name="%(app_label)s_%(class)s_related",
        help_text=u'Настоящий покупатель')
    money = models.PositiveIntegerField(verbose_name=u'Сумма', default=0)
    proxy = models.ForeignKey(Agent, verbose_name=u'Посредник', related_name="proxy_%(app_label)s_%(class)s_related",
        limit_choices_to={'pk__in': (1,)}, # Серверная керамика
        null=True, blank=True, help_text=u'например Серверная керамика')

    class Meta():
        verbose_name = u"накладная"
        verbose_name_plural = u"накладные"
        ordering = ['-date', '-number']

    @property
    def total(self):
        return reduce(lambda memo, x: memo + x['amount'], self.bill_sold_related.values('amount').all(), 0)

    @property
    def tara(self):
        return reduce(lambda memo, x: memo + x['tara'], self.bill_sold_related.values('tara').all(), 0)

    @property
    def opers(self):
        if not self.pk: return ()
        opers = []
        for o in self.bill_sold_related.select_related().all():
            opers.append(o)
            if o.transfer.count():
                opers.append(o.transfer.get())
        print opers
        return opers

    #    @property
    #    def money(self):
    #        return sum(map(lambda x: x['amount']*x['price'], self.bill_sold_related.values('amount','price')))

    def __unicode__(self):
        if self.pk:
            return u'Накладная № %d, %d' % (self.number, self.date.year)
        else:
            return u'Новая накладная'

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name, self.id)


class Transfer(Oper):
    """ Класс для операций перевода, представляет себя логическую операцию по продажи одной марки
    по цене другой, аналог скидки.
    Содержит только информацию о кол-ве и том кирпиче из которго совершается перевод, конечная
    точка перевода содержится по связи sold.
    Привязанн к накладной, т.к является операцией продажи. """

    doc = models.ForeignKey(Bill, blank=True, related_name="%(app_label)s_%(class)s_related", null=True,
        verbose_name=u'Накладная')


    class Meta():
        verbose_name = u"перевод"
        verbose_name_plural = u"переводы"

    def __unicode__(self):
        if self.pk:
            return u'Перевод %s' % self.brick
        else:
            return u'Новый перевод'


class Sold(Oper):
    """ Класс для операций отгруки, является аналогом строки в накладной.
    Сообщяет нам какой,сколько и по какой цене отгружает кирпич в накладной. """

    price = models.FloatField(u"Цена за единицу", help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery = models.FloatField(u"Цена доставки", blank=True, null=True, help_text=u'0 если доставки нет')
    doc = models.ForeignKey(Bill, blank=True, related_name="%(app_label)s_%(class)s_related", null=True,
        verbose_name=u'Накладная')
    transfer = models.ManyToManyField('Transfer', blank=True, related_name="%(app_label)s_%(class)s_related", null=True,
        verbose_name=u'Перевод', help_text=u'')
    #Куда
    class Meta():
        verbose_name = u"отгрузка"
        verbose_name_plural = u"отгрузки"

    def __unicode__(self):
        if self.pk:
            return u'Отгрузка %s' % self.brick
        else:
            return u'Новая отгрузка'


from whs.bill.signals import *