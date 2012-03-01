# -*- coding: utf-8 -*-
from whs.bill.models import Oper,Doc
from django.db import models
import pytils
from whs.brick.models import Brick

class Man(Doc):
    """Класс документа для учета прихода кирпича с производства"""
    class Meta():
            verbose_name = u"Производство"
            verbose_name_plural = u"Производства"

    def __unicode__(self):
        if self.pk:
            date = pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.date)
            return u'Принятие на склад от %s' % date
        else:
            return u'Новая партия с производства'

    @property
    def total(self):
        return reduce(lambda memo,x: memo+x['amount'] ,self.manufacture_add_related.values('amount').all(),0)

class Add(Oper):
    """Класс операций для документа"""
    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u"Кирпич",
        help_text=u'Выберите кирпич')
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)
    class Meta():
            verbose_name = u"Партия"
            verbose_name_plural = u"Партия"

    def __unicode__(self):
        if self.pk:
            return u'Партия %s' % self.brick
        else:
            return u'Новая партия'
