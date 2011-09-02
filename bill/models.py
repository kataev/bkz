# -*- coding: utf-8 -*-
from django.db import models

from whs.brick.models import Brick
from whs.agent.models import Agent

import pytils

class Oper(models.Model):
    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))
#    post_c=((False,u'Не проведенно'),(True,u'Проведенно'))
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

    def widget(self,selected_html='',as_tr=False,attrs={}):
        attrs={
            'selected_html':selected_html,
            'value':self.pk,
#            'name':self._meta.module_name,
            'amount':self.amount,
            'tara':self.tara,
            'info':unicode(self.info),
            'brick_css':self.brick.show_css(), 
            'brick':unicode(self.brick),
            'brick_value':self.brick.pk
        }
        attrs.update(self.attr)
        at = u''
        for a in attrs:
            at += u'%s="%s" ' %(unicode(a),unicode(attrs[a]))
#        if as_tr:
            template = u'<option %s >%s</option>' % (at,unicode(self))
#        else:
#            template = u'<div dojoType="whs.oper" %s>%s</div>' % (at,unicode(self))
        return template

class Doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))

    number=models.PositiveIntegerField(unique_for_year='doc_date',verbose_name=u'№ документа',help_text=u'Число')
    doc_date=models.DateField(u'Дата',help_text=u'Дата документа')
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
#    time_change=models.DateTimeField(auto_now=True)
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True
#        ordering = ['-doc_date']

class Sold(Oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"отгрузка"
            verbose_name_plural =  u"отгрузки"

    def __unicode__(self):
        return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)

    def get_absolute_url(self):
        if self.pk:
            return "/form/%s/%i/" % (self._meta.module_name,self.id)
        else:
            return "/form/%s/" % (self._meta.module_name)


class Transfer(Oper):
    sold = models.ForeignKey(Sold,blank=True,related_name="%(app_label)s_%(class)s_related",null=True,verbose_name=u'Отгрузка') #Куда

    @property
    def attr(self):
        if self.sold:
            return {'child':self.sold.pk}
        else:
            return {}

    class Meta():
            verbose_name = u"перевод"
            verbose_name_plural = u"переводы"

    def __unicode__(self):
        if self.sold is None:
            return u'Незаконченный перевод № %d из %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Перевод № %d из %s в %s, %d шт' % (self.pk,self.brick,self.sold.brick,self.amount)

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)


## Накладная
class Bill(Doc):
    agent = models.ForeignKey(Agent,verbose_name=u'КонтрАгент',related_name="%(app_label)s_%(class)s_related")
    solds = models.ManyToManyField(Sold,related_name="%(app_label)s_%(class)s_related",blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfers = models.ManyToManyField(Transfer,related_name="%(app_label)s_%(class)s_related",blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"накладная"
            verbose_name_plural = u"накладные"
            ordering = ['-doc_date']

    def __unicode__(self):
        if self.pk:
            return u'Накладная № %d от %s %s' % (self.number,pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc_date),self.agent.name[:50])
        else:
            return u'Накладная'

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)