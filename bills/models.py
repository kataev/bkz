# -*- coding: utf-8 -*-
from django.db import models

from whs.bricks.models import bricks
from whs.agents.models import agent

import pytils

class oper(models.Model):
    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))
#    post_c=((False,u'Не проведенно'),(True,u'Проведенно'))
    brick=models.ForeignKey(bricks,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
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
            'name':self._meta.module_name,
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
        if as_tr:
            template = u'<option dojoType="whs.oper_tr" %s >%s</option>' % (at,unicode(self))
        else:
            template = u'<div dojoType="whs.oper" %s>%s</div>' % (at,unicode(self))
        return template

class doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))

    number=models.PositiveIntegerField(unique=True,verbose_name=u'№ документа',help_text=u'Число')
    doc_date=models.DateField(u'Дата',help_text=u'Дата документа')
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
#    time_change=models.DateTimeField(auto_now=True)
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True
#        ordering = ['-doc_date']



class sold(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"
            verbose_name_plural =  u"Отгрузки"

    def __unicode__(self):
        return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)

    def get_absolute_url(self):
        if self.pk:
            return "/form/%s/%i/" % (self._meta.module_name,self.id)
        else:
            return "/form/%s/" % (self._meta.module_name)


class transfer(oper):
    sold = models.ForeignKey(sold,blank=True,null=True,verbose_name=u'Отгрузка') #Куда

    @property
    def attr(self):
        if self.sold:
            return {'child':self.sold.pk}
        else:
            return {}

    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = u"Переводы"

    def __unicode__(self):
        if self.sold is None:
            return u'Незаконченный перевод № %d из %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Перевод № %d из %s в %s, %d шт' % (self.pk,self.brick,self.sold.brick,self.amount)

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)


## Накладная
class bill(doc):
    agent = models.ForeignKey(agent,verbose_name=u'КонтрАгент')
    solds = models.ManyToManyField(sold,blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfers = models.ManyToManyField(transfer,blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"Накладная"
            verbose_name_plural = u"Накладные"
            ordering = ['-doc_date']

    def __unicode__(self):
        return u'Накладная № %d от %s %s' % (self.number,pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc_date),self.agent.name[:50])

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)

    def posting(self):
        transfers = self.transfers.all()
        solds = self.solds.all()

        errors= []
        for t in transfers: # Обрабатываем
            t.brick.total +=t.amount
            t.sold.brick.total -= t.amount
        for s in solds:
            s.brick.total -=s.amount

        for t in transfers: # Проверяем
            if t.brick.total < 0:
                error = {'brick':t.brick,'amount':t.brick.total*-1,'error':u'Не хватает кирпича','oper':t}
                errors.append(error)
            if t.sold.brick.total < 0:
                error = {'brick':t.sold.brick,'amount':t.sold.brick.total*-1,'error':u'Не хватает кирпича в принимащей строне',"oper":t}
                errors.append(error)
        for s in solds:
            if s.brick.total < 0:
                error = {'brick':s.brick,'amount':s.brick.total*-1,'error':u'Не хватает кирпича','oper':s}
                errors.append(error)
        if len(errors) > 0:
            return errors
        else:
            for t in transfers:
                t.brick.save()
                t.sold.brick.save()
                t.post=True

            for s in solds:
                s.brick.save()
                s.post=True
            self.draft=True
            return []

