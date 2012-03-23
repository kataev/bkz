# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

from whs.brick.models import *
from whs.agent.models import Agent, Seller

# Накладная
class Bill(models.Model):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель', related_name="%(app_label)s_%(class)s_related")
    seller = models.ForeignKey(Seller, verbose_name=u'Продавец', related_name="proxy_%(app_label)s_%(class)s_related",
        help_text=u'', default=350)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    reason = models.CharField(u'Основание', max_length=300, blank=True,
        help_text=u'Основание для выставления товарной накладной')
    type = models.CharField(u'Вид операции', max_length=300, blank=True, help_text=u'')

    class Meta():
        verbose_name = u"Накладная"
        verbose_name_plural = u"Накладные"
        ordering = ['-date', '-number']
        permissions = (
            ("view_bill", u"Может просматривать накладные"),
            )

    def __unicode__(self):
        if self.pk:
            return u'№ %d, %d' % (self.number, self.date.year)
        else:
            return u'Новая накладная'

    def get_absolute_url(self):
        return u"/%s/%d/%d/" % (self._meta.verbose_name, self.date.year, self.number)

    def opers(self):
        return list(self.bill_sold_related.all()) + list(
            self.bill_transfer_related.all()) + list(self.bill_pallet_related.all())

    @property
    def tara_return(self):
        return self.date + relativedelta(months=+1)

    @property
    def total(self):
        total = self.bill_sold_related.aggregate(models.Sum('amount')).get('amount__sum') or 0
        total += self.bill_transfer_related.aggregate(models.Sum('amount')).get('amount__sum') or 0
        return total

    @property
    def netto(self):
        return sum([x.netto for x in self.opers()]) or 0

    @property
    def brutto(self):
        return sum([x.brutto for x in self.opers()]) or 0

    @property
    def tara(self):
        t = 0
        for o in self.opers():
            t+= getattr(o,'tara',0)
        return t

    @property
    def items(self):
        return sum([x.items for x in self.opers()])

    @property
    def money(self):
        return sum([x.money for x in self.opers()])

    @property
    def nds(self):
        return sum([x.nds for x in self.opers()])

    @property
    def in_total(self):
        return sum([x.in_total for x in self.opers()])

    @property
    def pages(self):
        return int(len(self.opers())/6 + 1)

class BillMixin(object):
    @property
    def nomenclature(self):
        return self.brick.nomenclature

    @property
    def money(self):
        return self.amount * self.price

    @property
    def netto(self):
        return int(round(self.amount * self.brick.mass))

    @property
    def brutto(self):
        return self.netto + 20 * self.tara

    @property
    def okei(self):
        return 796

    @property
    def package(self):
        return u'поддон'

    @property
    def space(self):
        return 288

    @property
    def items(self):
        return self.space * self.tara

    @property
    def nds(self):
        return round(self.doc.seller.nds * self.money,2)

    @property
    def get_nds_display(self):
        nds = self.doc.seller.nds
        if nds == 0:
            return u'б/НДС'
        else:
            return str(float(nds))[2:]

    @property
    def in_total(self):
        return self.money + self.nds



class Sold(BillMixin,models.Model):
    """ Класс для операций отгруки, является аналогом строки в накладной.
Сообщяет нам какой,сколько и по какой цене отгружает кирпич в накладной. """
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич")
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
    delivery = models.FloatField(u"Цена доставки", default=0, help_text=u'0 если доставки нет')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Отгрузка"
        verbose_name_plural = u"Отгрузки"

    def __unicode__(self):
        if self.pk:
            return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Новая отгрузка'


class Transfer(BillMixin,models.Model):
    """ Класс для операций перевода, представляет себя логическую операцию по продажи одной марки
    по цене другой, аналог скидки.
    Содержит только информацию о кол-ве и том кирпиче из которго совершается перевод, конечная
    точка перевода содержится по связи sold.
    Привязанн к накладной, т.к является операцией продажи. """
    brick_from = models.ForeignKey(Brick, related_name="brick_from_%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич откуда")
    brick_to = models.ForeignKey(Brick, related_name="brick_to_%(app_label)s_%(class)s_related",
        verbose_name=u"Кирпич куда")
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
    delivery = models.FloatField(u"Цена доставки", default=0, help_text=u'0 если доставки нет')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Перевод"
        verbose_name_plural = u"Переводы"

    def __unicode__(self):
        if self.pk:
            return u'Из %s в %s, %d шт' % (self.brick_from, self.brick_to, self.amount)
        else:
            return u'Новый перевод'

    @property
    def brick(self):
        return self.brick_to


class Pallet(models.Model):
    """
    Поддоны при продаже
    """
    amount = models.PositiveIntegerField(u"Кол-во поддоннов")
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Поддон"
        verbose_name_plural = u"Поддоны"

    def __unicode__(self):
        if self.pk:
            return u'Поддоны %d шт' % self.amount
        else:
            return u'Продажа поддонов'

    @property
    def nomenclature(self):
        return dict(title=u'Поддоны - Возвратная тара',intcode=131)

    @property
    def netto(self):
        return 0

    @property
    def brutto(self):
        return 0

    @property
    def price(self):
        return 200.00

    @property
    def money(self):
        return self.amount * self.price

    @property
    def items(self):
        return self.amount

    @property
    def nds(self):
        return 0

    @property
    def in_total(self):
        return self.money