# -*- coding: utf-8 -*-
import datetime

from django.db import models

from constants import *
from bkz.utils import UrlMixin, ru_date
from whs.pdf import PalletMixin, SoldMixin, BillMixin


class Width(models.Model):
    """
    Сущность для номинальных размеров из ГОСТ 530-2007.
    """
    name = models.CharField(u'Вид изделия', max_length=30)
    label = models.CharField(u'Обозначение вида', max_length=6)
    size = models.CharField(u'Номинальные размеры', max_length=20)
    value = models.CharField(u'Обозначение размера', max_length=10)
    type = models.BooleanField(u'Тип', choices=((False, u'Кирпич'), (True, u'Камень')), )
    tts = models.IntegerField(u'Кол-во полуфабрика на ТТС', default=0)
    tto = models.IntegerField(u'Кол-во полуфабрика на ТТО', default=0)

    def __unicode__(self):
        return u'%s %s' % (self.value, self.name,)

    class Meta:
        ordering = ('pk',)
        verbose_name = u'Номинальный размер'
        verbose_name_plural = u'Номинальный размеры'


class Features(models.Model):
    """
    Сущность для хранения видов различных особенностей готовой продукции.
    """
    name = models.CharField(u'Имя', max_length=30)
    type = models.CharField(u'Сокращённое название', max_length=30)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.type)

    class Meta:
        ordering = ('type',)
        verbose_name = u'Особенности'
        verbose_name_plural = u'Особенности'


class Brick(models.Model, UrlMixin):
    """ Сущность для готовой продукции, содержит характеристики и текущий остатк """
    cavitation = models.PositiveIntegerField(u"Пустотелость", choices=cavitation_c, default=cavitation_c[0][0])
    color = models.PositiveIntegerField(u"Цвет", choices=color_c, default=color_c[0][0])
    mark = models.PositiveIntegerField(u"Марка", choices=mark_c, default=mark_c[0][0])
    width = models.ForeignKey('whs.Width', verbose_name=u'Размер')
    view = models.CharField(u"Вид", max_length=60, choices=view_c, default=view_c[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=ctype_c, default=ctype_c[0][0], blank=True)
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c, default=defect_c[0][0], blank=True)
    refuse = models.CharField(u"Особенности", max_length=10, choices=refuse_c, default=refuse_c[0][0], blank=True)
    frost_resistance = models.PositiveIntegerField(u"Морозостойкость", default=50, choices=frostresistance_c)
    cad = models.FloatField(u'Класс средней плотности', choices=cad_c)
    features = models.ManyToManyField(Features, verbose_name=u'Редкие особенности', null=True, blank=True)
    name = models.CharField(u"Наименование", max_length=160, default='',
                            help_text=u'Введите полное название продукции, для проверки')

    css = models.CharField(u"Стили", max_length=360, default=u'')
    label = models.CharField(u"Ярлык", max_length=660, default='')

    total = models.PositiveIntegerField(u"Остаток", default=0)
    mass = models.FloatField(u'Масса', default=0.0)

    nomenclature = models.ForeignKey('whs.Nomenclature', null=True, blank=True, verbose_name=u'Номенклатура')

    order = ('begin', 'add', 't_from', 't_to', 'sold', 'm_from', 'm_to', 'm_rmv', 'inv', 'total')

    def __unicode__(self):
        if not self.pk:
            return u'Новый кирпич'
        else:
            return self.label

    def make_label(self):
        return make_label(self)

    def make_css(self):
        return make_css(self)

    get_bricks_per_pallet = property(bricks_per_pallet)

    class Meta():
        ordering = BrickOrder
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'
        permissions = (("view_brick", u"Может просматривать таблицу с остатками"),)


class OldBrick(models.Model):
    """
    Сущность для хранения id записей продукции в старой базы.
    """
    brick = models.ForeignKey(Brick, related_name='oldbrick')
    old = models.IntegerField('ID кирпича в старой базе')
    prim = models.CharField(u"Имя", max_length=260, default='', help_text=u'Старое "имя"')


type_c = ((0, u'Юр.Лицо'), (1, u'Физ.лицо'))


class Agent(models.Model, UrlMixin):
    """
    Сущность контрагента.
    """
    name = models.CharField(u"Имя", max_length=400, db_index=True,
                            help_text=u'Название без юридической формы, без ООО, без ИП, без кавычек.')
    fullname = models.CharField(u"Полное имя", max_length=400, help_text=u'Название для накладных')
    form = models.IntegerField(u'Тип', choices=type_c, help_text=u'Выберите тип контрагента', default=0)

    address = models.CharField(u"Адрес", blank=True, max_length=200, help_text=u'Юридический адрес')
    phone = models.CharField(u"Телефон", blank=True, max_length=200)

    inn = models.CharField(u"Инн", blank=True, max_length=200)
    kpp = models.CharField(u'КПП', help_text=u'Введите код ОКПО', blank=True, max_length=200)

    bank = models.CharField(u"Банк", blank=True, max_length=200)
    ks = models.CharField(u"Корректиционный счет", blank=True, max_length=200)
    bic = models.CharField(u"Бик", blank=True, max_length=200)

    rs = models.CharField(u"Расчетный счет", blank=True, max_length=200)

    info = models.CharField(u'Примечание', max_length=600, blank=True, help_text=u'Любая полезная информация')
    type = models.CharField(u'Тип', max_length=600, blank=True, help_text=u'Тип контргаента')

    class Meta:
        verbose_name = u'Контрагент'
        verbose_name_plural = u'Контрагенты'

        permissions = (("view_agent", u"Может просматривать контрагентa"),)
        ordering = ('name', )

    def __unicode__(self):
        if self.pk:
            return self.name[:40]
        else:
            return u'Новый контрагент'


class Seller(models.Model, UrlMixin):
    """
    Сущность для продавца продукции.
    """
    agent = models.OneToOneField(Agent, verbose_name=u'Контрагент')
    director = models.CharField(u'Директор', max_length=200)
    buhgalter = models.CharField(u'Бухгалтер', max_length=200)
    dispetcher = models.CharField(u'Диспечер', max_length=200)
    nds = models.FloatField(u'НДС', default=0.18)

    def __unicode__(self):
        return self.agent.name[:40]

    class Meta:
        verbose_name = u'Продавец'
        verbose_name_plural = u'Продавецы'


class OldAgent(models.Model):
    """
    Сущность для хранения id записей контрагентов в старой базы.
    """
    agent = models.ForeignKey(Agent, related_name='oldagent')
    old = models.IntegerField('ID контрагентa в старой базе')


class Bill(UrlMixin, BillMixin, models.Model):
    """ Сущность накладных """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
                                         help_text=u'Число уникальное в этом году')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today(), db_index=True)
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель', related_name=u'bill_agents', help_text=u'', default=1)
    seller = models.ForeignKey(Seller, verbose_name=u'Продавец', help_text=u'', default=350,
                               related_name='bill_sallers')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    reason = models.CharField(u'Основание', max_length=300, blank=True,
                              help_text=u'Основание для выставления товарной накладной')
    type = models.CharField(u'Вид операции', max_length=300, blank=True)

    @property
    def bkz(self):
        return Seller.objects.get(pk=1)

    class Meta():
        verbose_name = u"Накладная"
        verbose_name_plural = u"Накладные"
        ordering = ['-date', '-number']

    solds = []

    def __unicode__(self):
        if self.pk:
            return u'№ %d, %d' % (self.number, self.date.year)
        else:
            return u'Новая накладная'


class Pallet(PalletMixin, models.Model):
    """ Сущность строки в накладной с поддонами """
    amount = models.PositiveIntegerField(u"Кол-во поддоннов", default=1)
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.',
                              default=200)
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="pallets", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Поддон"
        verbose_name_plural = u"Поддоны"

    def __unicode__(self):
        if self.pk:
            return u'Поддоны - %d шт' % self.amount
        else:
            return u'Продажа поддонов'


class Sold(SoldMixin, models.Model):
    """Сущность строки с продукцией в накладной """
    brick_from = models.ForeignKey(Brick, related_name="sold_brick_from",
                                   verbose_name=u"Перевод", blank=True, null=True)
    brick = models.ForeignKey(Brick, related_name="sold_brick", verbose_name=u"Кирпич")
    batch_number = models.PositiveSmallIntegerField(u'Партия', null=True, blank=True)
    batch_year = models.PositiveSmallIntegerField(u'Год партии', null=True, blank=True,
                                                  default=datetime.date.today().year)
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции', default=1)
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.',
                              default=0)
    delivery = models.FloatField(u"Цена доставки", default=0, help_text=u'0 если доставки нет')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="solds", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Отгрузка"
        verbose_name_plural = u"Отгрузки"
        ordering = ['-doc__date', '-doc__number']

    def __unicode__(self):
        if self.pk:
            if self.brick_from:
                return u'%s < %s - %d шт' % (self.brick, self.brick_from, self.amount)
            else:
                return u'%s - %d шт' % (self.brick, self.amount)
        else:
            return u'Новая отгрузка'

    @property
    def css(self):
        if self.brick_from:
            return self.brick_from.css
        else:
            return self.brick.css


class Nomenclature(models.Model):
    """" Номенклатурный номер для продукции, необхоидмо для связи с бухгалтерией. Коды берутся с id номенклатуры из базы 1с """
    title = models.CharField(u"Наименование", max_length=200, blank=False, unique=True)
    code = models.CharField(u"Код", max_length=11, blank=False, unique=True)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.title)

    class Meta:
        verbose_name = u'Номенклатура'
        verbose_name_plural = u'Номенклатуры'


class BuhAgent(models.Model):
    """Содержит информацию о id запией контрагентов в бухгалтерской базе 1с """
    agent = models.ForeignKey(Agent, related_name='buhagent')
    code = models.CharField(u"Код", max_length=11, blank=False, unique=True)


sorting_type_c = ((0, u'В цех'), (1, u'Из цеха'), (2, u'Списанно'))


class Sorting(models.Model, UrlMixin):
    """ Сущность документа для учета сортировки кипича из одного товара в другой """
    type = models.IntegerField(u'Тип', choices=sorting_type_c)
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    brick = models.ForeignKey(Brick, related_name="sorting", verbose_name=u"Кирпич")
    amount = models.PositiveIntegerField(u"Кол-во", help_text=u'Кол-во кирпича для операции', default=1)

    batch_number = models.PositiveSmallIntegerField(u'Партия', null=True, blank=True)
    batch_year = models.PositiveSmallIntegerField(u'Год партии', null=True, blank=True,
                                                  default=datetime.date.today().year)

    source = models.ForeignKey('self', null=True, blank=True, related_name='sorted')

    class Meta():
        verbose_name = u"Сортировка"
        verbose_name_plural = u"Сортировка"

    @property
    def total(self):
        return self.amount - getattr(self, 'sorted__amount__sum', 0)

    @property
    def get_days_in_work(self):
        if self.source:
            return (self.date - self.source.date).days

    def get_type_class_display(self):
        if self.type == 0:
            return 'info'
        elif self.type == 1:
            return 'success'
        elif self.type == 2:
            return 'error'

    def get_batch_display(self):
        if datetime.date.today().year != self.batch_year:
            return '%d, %s' % (self.batch_number, self.batch_year)
        else:
            return self.batch_number

    def __unicode__(self):
        if self.pk:
            return u'%s %s, %s - %d шт' % (self.get_type_display(), ru_date(self.date), self.brick, self.amount)
        else:
            return u'Новая сортировка'


class Inventory(models.Model, UrlMixin):
    """ Сущность инвентаризации, отражается на акт о инвентаризации"""
    date = models.DateField(u'Дата', default=datetime.date.today())
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')

    class Meta():
        verbose_name = u"Инвентаризация"
        verbose_name_plural = u"Инвентаризации"
        permissions = (("view_inventory", u"Может просматривать инвентаризацию"),)

    def __unicode__(self):
        if self.pk:
            return u'от %s' % self.date
        else:
            return u'Новая инвентаризация'


class Write_off(models.Model):
    """ Сущность для одной записи в акте о инвентаризация """
    brick = models.ForeignKey(Brick, related_name="write_off", verbose_name=u"Кирпич")
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции', default=1)
    doc = models.ForeignKey(Inventory, blank=False, related_name="write_off", null=False)

    class Meta():
        verbose_name = u"Списанние"
        verbose_name_plural = u"Списания"

    def __unicode__(self):
        if self.pk:
            return u'%s - %d шт' % (self.brick, self.amount)
        else:
            return u'Списание'
