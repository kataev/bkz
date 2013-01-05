# -*- coding: utf-8 -*-
import datetime

from django.db import models

from constants import *
from bkz.utils import UrlMixin,ru_date
from whs.pdf import PalletMixin, SoldMixin, BillMixin

class Width(models.Model):
    name = models.CharField(u'Вид изделия',max_length=30)
    label = models.CharField(u'Обозначение вида',max_length=6)
    size = models.CharField(u'Номинальные размеры',max_length=20)
    value = models.CharField(u'Обозначение размера',max_length=10)
    type = models.BooleanField(u'Тип',choices=((False,u'Кирпич'),(True,u'Камень')),)

    def __unicode__(self):
        return u'%s %s' % (self.value,self.name,)
    class Meta:
        ordering = ('pk',)

class Features(models.Model):
    name = models.CharField(u'Имя',max_length=30)
    type = models.CharField(u'Сокрашение',max_length=30)

    def __unicode__(self):
        return '%s (%s)' % (self.name,self.type)
    class Meta:
        ordering = ('type',)

class Brick(models.Model,UrlMixin):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """
    cavitation = models.PositiveIntegerField(u"Пустотелость", choices=cavitation_c, default=cavitation_c[0][0])
    color = models.PositiveIntegerField(u"Цвет", choices=color_c, default=color_c[0][0])
    mark = models.PositiveIntegerField(u"Марка", choices=mark_c, default=mark_c[0][0])
    width = models.ForeignKey('whs.Width',verbose_name=u'Размер')
    ww = models.FloatField(u"Размер", choices=width_c, default=width_c[0][0])
    view = models.CharField(u"Вид", max_length=60, choices=view_c, default=view_c[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=ctype_c, default=ctype_c[0][0],blank=True)
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c, default=defect_c[0][0],blank=True)
    refuse = models.CharField(u"Особенности", max_length=10, choices=refuse_c, default=refuse_c[0][0],blank=True)
    frost_resistance = models.PositiveIntegerField(u"Морозостойкость",default=50,choices=frostresistance_c)
    cad = models.FloatField(u'Класс средней плотности',choices=cad_c)
    features = models.ManyToManyField(Features,verbose_name=u'Редкие особенности',null=True,blank=True)
    name = models.CharField(u"Наименование", max_length=160, default='', help_text=u'Введите полное название продукции, для проверки')

    css = models.CharField(u"Css", max_length=360, default=u'')
    label = models.CharField(u"Ярлык", max_length=660, default='')

    total = models.PositiveIntegerField(u"Остаток", default=0)
    mass = models.FloatField(u'Ожидамая масса',default=0.0)

    nomenclature = models.ForeignKey('whs.Nomenclature', null=True, blank=True, verbose_name=u'Номенклатура')

    order = ('begin','add','t_from','t_to','sold','m_from','m_to','m_rmv','inv','total')

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def make_label(self):
        return make_label(self)

    def make_css(self):
        return make_css(self)

    class Meta():
        ordering = BrickOrder
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'
        permissions = (("view_brick", u"Может просматривать таблицу с остатками"),)

class OldBrick(models.Model):
    brick = models.ForeignKey(Brick,related_name='oldbrick')
    old = models.IntegerField('Старое ID')
    prim = models.CharField(u"Имя", max_length=260, default='', help_text=u'Старое "имя"')

type_c = ((0,u'Юр.Лицо'),(1,u'Физ.лицо'))

class Agent(models.Model,UrlMixin):
    name = models.CharField(u"Имя",max_length=400,db_index=True,
        help_text=u'Название без юридической формы, без ООО, без ИП, без кавычек.')
    fullname = models.CharField(u"Полное имя",max_length=400,help_text=u'Название для накладных')
    form = models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)

    address = models.CharField(u"Адрес",blank=True,max_length=200,help_text=u'Юридический адрес')
    phone = models.CharField(u"Телефон",blank=True,max_length=200)

    inn = models.CharField(u"Инн",blank=True,max_length=200)
    kpp = models.CharField(u'КПП',help_text=u'Введите код ОКПО',blank=True,max_length=200)

    bank = models.CharField(u"Банк",blank=True,max_length=200)
    ks = models.CharField(u"Корректиционный счет",blank=True,max_length=200)
    bic = models.CharField(u"Бик",blank=True,max_length=200)

    rs=models.CharField(u"Расчетный счет",blank=True,max_length=200)

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

class Seller(Agent,UrlMixin):
    director = models.CharField(u'Директор',max_length=200)
    buhgalter = models.CharField(u'Бухгалтер',max_length=200)
    dispetcher = models.CharField(u'Диспечер',max_length=200)
    nds = models.FloatField(u'НДС',default=0.18)

    class Meta:
        verbose_name=u'Продавец'
        verbose_name_plural=u'Продавецы'
        ordering = ('name', )

class OldAgent(models.Model):
    agent = models.ForeignKey(Agent,related_name='oldagent')
    old = models.IntegerField('Старое ID')


class Bill(UrlMixin, BillMixin, models.Model):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today(),db_index=True)
    agent = models.ForeignKey(Agent, verbose_name=u'Покупатель',related_name=u'bill_agents',help_text=u'',default=1)
    seller = models.ForeignKey(Seller, verbose_name=u'Продавец', help_text=u'', default=350,related_name='bill_sallers')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    reason = models.CharField(u'Основание', max_length=300, blank=True,
        help_text=u'Основание для выставления товарной накладной')
    type = models.CharField(u'Вид операции', max_length=300, blank=True)

    @property
    def bkz(self):
        return Seller.objects.get(pk=1206)

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
    """ Поддоны при продаже """
    amount = models.PositiveIntegerField(u"Кол-во поддоннов")
    poddon = models.PositiveIntegerField(u"Тип поддона", choices=poddon_c, default=352)
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.',default=200)
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

class Sold(SoldMixin,models.Model):
    brick_from = models.ForeignKey(Brick, related_name="sold_brick_from",
        verbose_name=u"Перевод",blank=True,null=True)
    brick = models.ForeignKey(Brick, related_name="sold_brick", verbose_name=u"Кирпич")
    batch_number = models.PositiveSmallIntegerField(u'Партия',null=True, blank=True)
    batch_year = models.PositiveSmallIntegerField(u'Год партии',null=True, blank=True,default=datetime.date.today().year)
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.',default=0)
    delivery = models.FloatField(u"Цена доставки", default=0, help_text=u'0 если доставки нет')
    info = models.CharField(u'Примечание', max_length=300, blank=True, help_text=u'Любая полезная информация')
    doc = models.ForeignKey(Bill, related_name="solds", verbose_name=u'Накладная')

    class Meta():
        verbose_name = u"Отгрузка"
        verbose_name_plural = u"Отгрузки"
        ordering = ['-doc__date','-doc__number']

    def __unicode__(self):
        if self.pk:
            if self.brick_from:
                return u'%s < %s - %d шт' % (self.brick,self.brick_from, self.amount)
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
    title = models.CharField(u"Наименование", max_length=200,blank=False,unique=True)
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)

    def __unicode__(self):
        return u'%s - %s' % (self.code,self.title)

class BuhAgent(models.Model):
    agent = models.ForeignKey(Agent,related_name='buhagent')
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)


sorting_type_c = ((0,u'В цех'),(1,u'Из цеха'),(2,u'Списанно'))

class Sorting(models.Model,UrlMixin):
    """ Класс документа для учета сортировки кипича из одного товара в другой """
    type = models.IntegerField(u'Тип',choices=sorting_type_c)
    date = models.DateField(u'Дата', help_text=u'Дата документа', default=datetime.date.today())
    brick = models.ForeignKey(Brick, related_name="sorting", verbose_name=u"Кирпич")
    amount = models.PositiveIntegerField(u"Кол-во", help_text=u'Кол-во кирпича для операции')

    batch_number = models.PositiveSmallIntegerField(u'Партия',null=True, blank=True)
    batch_year = models.PositiveSmallIntegerField(u'Год партии',null=True, blank=True,default=datetime.date.today().year)

    source = models.ForeignKey('self',null=True,blank=True,related_name='sorted')

    class Meta():
        verbose_name = u"Сортировка"

    @property
    def total(self):
        return self.amount - getattr(self,'sorted__amount__sum',0)

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
            return '%d, %s' % (self.batch_number,self.batch_year)
        else: return self.batch_number

    def __unicode__(self):
        if self.pk:
            return u'%s %s, %s - %d шт' % (self.get_type_display(),ru_date(self.date),self.brick,self.amount)
        else:
            return u'Новая сортировка'

class Inventory(models.Model, UrlMixin):
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
    brick = models.ForeignKey(Brick, related_name="write_off", verbose_name=u"Кирпич")
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    doc = models.ForeignKey(Inventory, blank=False, related_name="write_off", null=False)

    class Meta():
        verbose_name = u"Списанние"
        verbose_name_plural = u"Списания"

    def __unicode__(self):
        if self.pk: return u'%s - %d шт' % (self.brick, self.amount)
        else: return u'Списание'
