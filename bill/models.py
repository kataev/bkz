# -*- coding: utf-8 -*-
from django.db import models
from whs.brick.models import Brick
from whs.agent.models import Agent
import datetime

poddon_c = ((288, u'Маленький поддон'), (352, u'Обычный поддон'))

class Oper(models.Model):
    """ Абстрактный класс для всех операций """

    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

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

bill_type_c = (('pickup', 'Самовывоз'), (''))

## Накладная
class Bill(Doc):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель', related_name="%(app_label)s_%(class)s_related",
        help_text=u'Настоящий покупатель')
    seller = models.ForeignKey(Agent, verbose_name=u'Продавец', related_name="proxy_%(app_label)s_%(class)s_related",
        limit_choices_to={'pk__in': (1, 350)}, # Серверная керамика
        null=False, blank=False, help_text=u'например Серверная керамика')

    reason = models.CharField(u'Основание', max_length=300, blank=True,
        help_text=u'Основание для выставления товарной накладной')
    type = models.CharField(u'Вид операции', max_length=300, blank=True, help_text=u'')

    class Meta():
        verbose_name = u"Накладная"
        verbose_name_plural = u"Накладные"
        ordering = ['-date', '-number']

#    @property
#    def total(self):
#        if self.pk: return sum([x[0] for x in self.bill_sold_related.values_list('amount')])
#        else: return 0
#
#    @property
#    def tara(self):
#        if self.pk: return sum([x[0] for x in self.bill_sold_related.values_list('tara')])
#        else: return 0
#
#    @property
#    def tara_return(self):
#        return self.date + datetime.timedelta(days=30)
#
#    @property
#    def opers(self):
#        if not self.pk: return ()
#        opers = []
#        return self.bill_sold_related.all()
#
#    @property
#    def money(self):
#        if self.pk: return sum([x[0] * x[1] for x in self.bill_sold_related.values_list('amount', 'price')])
#        else: return 0

    def __unicode__(self):
        if self.pk:
            return u'Накладная № %d, %d' % (self.number, self.date.year)
        else:
            return u'Новая накладная'

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name, self.id)


class Sold(Oper):
    """ Класс для операций отгруки, является аналогом строки в накладной.
Сообщяет нам какой,сколько и по какой цене отгружает кирпич в накладной. """

    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
    delivery = models.FloatField(u"Цена доставки", blank=True, null=True, help_text=u'0 если доставки нет')
    doc = models.ForeignKey(Bill, blank=True, related_name="%(app_label)s_%(class)s_related", null=True,
        verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Отгрузка"
        verbose_name_plural = u"Отгрузки"

    def __unicode__(self):
        if self.pk:
            return u'Отгрузка %s, %d шт' % (self.brick,self.amount)
        else:
            return u'Новая отгрузка'

#    @property
#    def transfer_amount(self):
#        if self.pk: return sum([x[0] for x in self.transfer.values_list('amount')])
#        else: return 0
#
#    @property
#    def places(self):
#        return self.poddon * self.tara
#
#    @property
#    def money(self):
#        return self.amount * self.price


class Transfer(Sold):
    """ Класс для операций перевода, представляет себя логическую операцию по продажи одной марки
    по цене другой, аналог скидки.
    Содержит только информацию о кол-ве и том кирпиче из которго совершается перевод, конечная
    точка перевода содержится по связи sold.
    Привязанн к накладной, т.к является операцией продажи. """

    brick_from = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич откуда", help_text=u'Выберите кирпич')

    class Meta():
        verbose_name = u"Перевод"
        verbose_name_plural = u"Переводы"

    def __unicode__(self):
        if self.pk:
            return u'Перевод %s' % self.brick
        else:
            return u'Новый перевод'


