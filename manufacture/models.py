# -*- coding: utf-8 -*-
from whs.bill.models import Oper,Doc
from django.db import models
import pytils

class Man(Doc):
    """Класс документа для учета прихода кирпича с производства"""
    class Meta():
            verbose_name = u"Производство за день"
            verbose_name_plural = u"Производство за день"


    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'Принятие на склад от %s' % date
        else:
            return u'Новая партия с производства'
    def get_absolute_url(self):
        return '/%s/%d/' % (self._meta.module_name.lower(),self.pk)

    @property
    def opers(self):
        return list(self.manufacture_add_related.all())

    @property
    def total(self):
        return reduce(lambda memo,x: memo+x['amount'] ,self.manufacture_add_related.values('amount').all(),0)

class Add(Oper):
    """Класс операций для документа"""
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
            verbose_name = u"Произведённый кирпич"
            verbose_name_plural = u"Произведённые кирпичи"

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc.date)
            return u'Операция принятия на склад от %s' % date
        else:
            return u'Новая операция'
