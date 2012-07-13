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
    agent = models.ForeignKey('sale.Agent', verbose_name=u'Покупатель',related_name=u'bill_agents')
    seller = models.ForeignKey('sale.Seller', verbose_name=u'Продавец', help_text=u'', default=350,related_name='bill_sallers')
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
        permissions = (
            ("view_bill", u"Может просматривать накладные"),
            )

    solds = []

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
    brick_from = models.ForeignKey(Brick, related_name="sold_brick_from",
        verbose_name=u"Перевод",blank=True,null=True)
    batch_from = models.CommaSeparatedIntegerField(u'Номера партий до перевода', blank=True, null=True,max_length=600)
    brick = models.ForeignKey(Brick, related_name="sold_brick", verbose_name=u"Кирпич")
    batch = models.IntegerField(u'Номер партии',null=True, blank=True)
    tara = models.PositiveIntegerField(u"Кол-во поддонов", default=0)
    amount = models.PositiveIntegerField(u"Кол-во кирпича", help_text=u'Кол-во кирпича для операции')
    price = models.FloatField(u"Цена за единицу", help_text=u'Цена за шт. Можно прокручивать колёсиком мыши.')
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
                return u'%s < %s, %d шт' % (self.brick,self.brick_from, self.amount)
            else:
                return u'%s, %d шт' % (self.brick, self.amount)
        else:
            return u'Новая отгрузка'

class Pallet(PalletMixin, models.Model):
    """
    Поддоны при продаже
    """
    number = models.PositiveIntegerField(unique_for_year='date', verbose_name=u'№ документа',
        help_text=u'Число уникальное в этом году')
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
            return u'Поддоны %d шт' % self.amount
        else:
            return u'Продажа поддонов'

type_c = ((0,u'Юр.Лицо'),(1,u'Физ.лицо'))

class Agent(models.Model):
    name = models.CharField(u"Имя",max_length=400,
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

    def get_absolute_url(self):
        return reverse('sale:Agent',kwargs=dict(id=self.pk))

class OldAgent(Agent):
    old = models.IntegerField('Старое ID')

class Seller(Agent):
    director_name = models.CharField(u'Должность директора',max_length=200)
    director = models.CharField(u'Директор',max_length=200)
    buhgalter_name = models.CharField(u'Должность бухгалтер',max_length=200)
    buhgalter = models.CharField(u'Бухгалтер',max_length=200)
    dispetcher_name = models.CharField(u'Должность диспечера',max_length=200)
    dispetcher = models.CharField(u'Диспечер',max_length=200)
    nds = models.FloatField(u'НДС',default=0.18)

    def get_absolute_url(self):
        return reverse('sale:Seller',kwargs=dict(id=self.pk))

    class Meta:
        verbose_name=u'Продавец'
        verbose_name_plural=u'Продавецы'


        ordering = ('name', )

class Nomenclature(models.Model):
    title = models.CharField(u"Наименование", max_length=200,blank=False,unique=True)
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)

    def __unicode__(self):
        return u'%s - %s' % (self.code,self.title)

    def intcode(self):
        return int(self.code)

class BuhAgent(Agent):
    code = models.CharField(u"Код", max_length=11,blank=False,unique=True)



class Price(models.Model):
    date = models.DateField(u'Дата')
    brick = models.ForeignKey(Brick,verbose_name=u'Кирпич')
    price = models.FloatField(u'Цена')