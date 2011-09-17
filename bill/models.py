# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from django.contrib import admin
from whs.brick.models import Brick
from whs.agent.models import Agent
import pytils
import datetime

class Oper(models.Model):
    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))
    brick=models.ForeignKey(Brick,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
    amount=models.PositiveIntegerField(u"Кол-во кирпича",help_text=u'Кол-во кирпича для операции')
    tara=models.PositiveIntegerField(u"Кол-во поддонов",default=0)
    poddon=models.PositiveIntegerField(u"Тип поддона",choices=poddon_c,default=1)
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
    post=models.BooleanField(u'Проведенно?',default=False)
    # DRAFT ДЛЯ ПРОСТОТЫ!!!! ПОДУМАТЬ!!!
    attr={}
    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/%s/%d/' % (self._meta.module_name.lower(),self.pk)

    def widget(self,selected_html='',as_tr=False,attrs={}):
        attrs={
#            'selected_html':selected_html,
            'value':self.pk,
            'name':self._meta.module_name.lower(),
            'amount':self.amount,
            'tara':self.tara,
            'info':self.info,
            'brick_css':self.brick.show_css(), 
            'brick':self.brick,
            'brick_value':self.brick.pk,
            'title':self
        }
        attrs.update(self.attr)
        at = u''
        for a in attrs:
            at += u'%s="%s" ' %(unicode(a),unicode(attrs[a]))
#        if as_tr:
        template = u'<tr %s dojoType="whs.oper.tr" ></tr>' % at
#        else:
#            template = u'<div dojoType="whs.oper" %s>%s</div>' % (at,unicode(self))
        return template

class Doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))
    date=models.DateField(u'Дата',help_text=u'Дата документа',default=datetime.date.today())
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True

class Sold(Oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')

    class Meta():
            verbose_name = u"отгрузка"
            verbose_name_plural =  u"отгрузки"

    def __unicode__(self):
        if self.pk:
            return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Новая отгрузка'

class Transfer(Oper):
    sold = models.ForeignKey(Sold,blank=True,related_name="%(app_label)s_%(class)s_related",null=True,verbose_name=u'Отгрузка') #Куда

    class Meta():
            verbose_name = u"перевод"
            verbose_name_plural = u"переводы"

    def __unicode__(self):
        if self.pk:
            if self.sold is None:
                return u'Незаконченный перевод № %d из %s, %d шт' % (self.pk,self.brick,self.amount)
            else:
                return u'Перевод № %d из %s в %s, %d шт' % (self.pk,self.brick,self.sold.brick,self.amount)
        else:
            return u'Новый перевод'

## Накладная
class Bill(Doc):
    """
    Bill doc
    """
    number=models.PositiveIntegerField(unique_for_year='date',verbose_name=u'№ документа',help_text=u'Число')
    agent = models.ForeignKey(Agent,verbose_name=u'КонтрАгент',related_name="%(app_label)s_%(class)s_related")
    sold = models.ManyToManyField(Sold,related_name="%(app_label)s_%(class)s_related",blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfer = models.ManyToManyField(Transfer,related_name="%(app_label)s_%(class)s_related",blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"накладная"
            verbose_name_plural = u"накладные"
            ordering = ['-date','-number']

    def money(self):
        return sum(map(lambda x: x['amount']*x['price'], self.sold.values('amount','price')))
        
    def str_date(self):
        return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)

    def __unicode__(self):
        if self.pk:
            return u'Накладная № %d от %s %s' % (self.number,self.str_date(),self.agent.name[:50])
        else:
            return u'Новая накладная'

    def get_absolute_url(self):
        return "/%s/%i/" % (self._meta.module_name,self.id)


admin.site.register(Bill)
admin.site.register(Sold)
admin.site.register(Transfer)