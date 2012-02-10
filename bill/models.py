# -*- coding: utf-8 -*-
from django.db import models
from whs.brick.models import Brick
from whs.agent.models import Agent
import pytils
import datetime

class Oper(models.Model):
    """ Абстрактный класс для всех операций """
    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))

    brick=models.ForeignKey(Brick,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
    amount=models.PositiveIntegerField(u"Кол-во кирпича",help_text=u'Кол-во кирпича для операции')
    tara=models.PositiveIntegerField(u"Кол-во поддонов",default=0)
    poddon=models.PositiveIntegerField(u"Тип поддона",choices=poddon_c,default=1)
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')

    def get_id(self):
        return u'%s.%s__%d' % (self._meta.app_label,self._meta.module_name,self.pk)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/%s/%d/' % (self._meta.module_name.lower(),self.pk)

class Doc(models.Model):
    """ Абстрактный класс для документов. """
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))
    date=models.DateField(u'Дата',help_text=u'Дата документа',default=datetime.date.today())
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True

## Накладная
class Bill(Doc):
    """ Накладная, документ который используется при отгрузке кирпича покупателю
    Основа продажи, на него ссылаются операции продажи - Sold && Transfer. """
    number=models.PositiveIntegerField(unique_for_year='date',verbose_name=u'№ документа',help_text=u'Число уникальное в этом году')
    agent = models.ForeignKey(Agent,verbose_name=u'Покупатель',related_name="%(app_label)s_%(class)s_related",
                              help_text=u'Настоящий покупатель')
    money=models.PositiveIntegerField(verbose_name=u'Сумма',default=0)
    proxy = models.ForeignKey(Agent,verbose_name=u'Посредник',related_name="proxy_%(app_label)s_%(class)s_related",
                              limit_choices_to = {'pk__in':(1,)}, # Серверная керамика
                              null=True,blank=True,help_text=u'например Серверная керамика')

    class Meta():
            verbose_name = u"накладная"
            verbose_name_plural = u"накладные"
            ordering = ['-date','-number']

    def solds(self):
        return map(lambda x: (x.brick.label,x.brick.pk,x.brick.css,x.amount),self.bill_sold_related.all())

    def set_money(self):
        """ Метод для обновления информации о кол-ве денег. Вызывается через сигнал после сохранение SOLD """

        self.money = sum(map(lambda x: x['amount']*x['price'], self.bill_sold_related.values('amount','price')))
        self.save()

    def date_ru(self):
        return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)

    def __unicode__(self):
        if self.pk:
            date = self.date_ru()
            return u'Накладная № %d от %s %s' % (self.number,date,unicode(self.agent)[:50])
        else:
            return u'Новая накладная'

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name,self.id)

class Transfer(Oper):
    """ Класс для операций перевода, представляет себя логическую операцию по продажи одной марки
    по цене другой, аналог скидки.
    Содержит только информацию о кол-ве и том кирпиче из которго совершается перевод, конечная
    точка перевода содержится по связи sold.
    Привязанн к накладной, т.к является операцией продажи. """

    doc = models.ForeignKey(Bill,blank=True,related_name="%(app_label)s_%(class)s_related",null=True,verbose_name=u'Накладная')
    sold = models.ForeignKey('Transfer',blank=True,related_name="%(app_label)s_%(class)s_related",null=True,verbose_name=u'Отгрузка')

    class Meta():
            verbose_name = u"перевод"
            verbose_name_plural = u"переводы"

    def __unicode__(self):
        if self.pk:
            return u'Перевод из %s, %d шт' % (self.brick,self.amount)
        else:
            return u'Новый перевод'

class Sold(Oper):
    """ Класс для операций отгруки, является аналогом строки в накладной.
    Сообщяет нам какой,сколько и по какой цене отгружает кирпич в накладной. """

    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
    doc = models.ForeignKey(Bill,blank=True,related_name="%(app_label)s_%(class)s_related",null=True,verbose_name=u'Накладная')
     #Куда
    class Meta():
            verbose_name = u"отгрузка"
            verbose_name_plural =  u"отгрузки"

    def __unicode__(self):
        if self.pk:
            return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Новая отгрузка'

#@receiver(post_save,sender=Sold)
#def money(*args,**kwargs):
#    kwargs['instance'].doc.set_money()

#@receiver(post_save,sender=Sold)
#def brick_total_actualizer(instance, created, *args,**kwargs):
#    model = instance
#    if created:
#        brick = Brick.objects.get(pk=model.brick.pk)
#        brick.total-=model.amount
#        brick.save()

from whs.bill.sygnals import *