# -*- coding: utf-8 -*-
import datetime

from whs.brick.models import *

from sale.pdf import OperationsMixin, BillMixin, PalletMixin


# Накладная
class Bill(BillMixin, models.Model):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    agent = models.ForeignKey('sale.Agent', verbose_name=u'Покупатель', related_name="%(app_label)s_%(class)s_related")
    seller = models.ForeignKey('sale.Seller', verbose_name=u'Продавец', related_name="proxy_%(app_label)s_%(class)s_related",
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
        return reverse('sale:Bill-year',kwargs=dict(year=self.date.year, number=self.number))


class Sold(OperationsMixin,models.Model):
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


class Transfer(OperationsMixin,models.Model):
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


class Pallet(PalletMixin, models.Model):
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

type_c = ((0,u'Юр.Лицо'),(1,u'Физ.лицо'))

class Agent(models.Model):
    name = models.CharField(u"Имя",max_length=400,
        help_text=u'Название без юридической формы, без ООО, без ИП, без кавычек.')
    fullname = models.CharField(u"Полное имя",max_length=400,help_text=u'Название для накладных')
    type = models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)

    address = models.CharField(u"Адрес",blank=True,max_length=200,help_text=u'Юридический адрес')
    phone = models.CharField(u"Телефон",blank=True,max_length=200)

    inn = models.CharField(u"Инн",blank=True,max_length=200)
    kpp = models.CharField(u'КПП',help_text=u'Введите код ОКПО',blank=True,max_length=200)

    bank = models.CharField(u"Банк",blank=True,max_length=200)
    ks = models.CharField(u"Корректиционный счет",blank=True,max_length=200)
    bic = models.CharField(u"Бик",blank=True,max_length=200)

    rs=models.CharField(u"Расчетный счет",blank=True,max_length=200)

    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')

    class Meta:
        verbose_name=u'Контрагент'
        verbose_name_plural=u'Контрагенты'
        permissions = (("view_agent", u"Может просматривать контрагентa"),)
        ordering = ('name', )

    def __unicode__(self):
        if self.pk:
            return self.name[:40]
        else:
            return u'Новый контрагент'

    def get_absolute_url(self):
        return reverse('sale:Agent',kwargs=dict(id=self.pk))

class OldAgent(Agent):
    old = models.IntegerField('Старое ID')

class People(models.Model):
    name = models.CharField(u"Имя",max_length=400)
    official = models.CharField(u"Должность",max_length=400)

    class Meta:
        verbose_name=u'Человек'
        verbose_name_plural=u'Люди'

class Seller(Agent):
    director = models.ForeignKey(People, related_name="%(app_label)s_%(class)s_director_related", verbose_name=u'Директор')
    buhgalter = models.ForeignKey(People, related_name="%(app_label)s_%(class)s_buhgalter_related", verbose_name=u'Бухгалтер')
    dispetcher = models.ForeignKey(People, related_name="%(app_label)s_%(class)s_dispetcher_related", verbose_name=u'Диспечер')

    class Meta:
        verbose_name=u'Продавец'
        verbose_name_plural=u'Продавецы'

        ordering = ('name', )

    @property
    def nds(self):
        return 0.18

class Nomenclature(models.Model):
    title = models.CharField(u"Наименование", max_length=200,blank=False,unique=True)
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)

    def __unicode__(self):
        return u'%s - %s' % (self.code,self.title)

    def intcode(self):
        return int(self.code)

class BuhAgent(Agent):
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)