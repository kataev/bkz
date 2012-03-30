# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from constants import *

class Brick(models.Model):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """

    color = models.PositiveIntegerField(u"Цвет", choices=color, default=color[0][0])
    mark = models.PositiveIntegerField(u"Марка", choices=mark, default=mark[0][0])
    weight = models.FloatField(u"Ширина", choices=weight, default=weight[0][0])
    view = models.CharField(u"Вид", max_length=60, choices=view, default=view[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=color_type, default=color_type[0][0],blank=True)
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect, default=defect[0][0],blank=True)
    refuse = models.CharField(u"Особенности", max_length=10, choices=refuse, default=refuse[0][0],blank=True)
    features = models.CharField(u"Редкие особенности", max_length=60, blank=True, help_text=u'Oттенки, тычки и прочее')
    name = models.CharField(u"Имя", max_length=160, default='', help_text=u'Полное название продукции')

    css = models.CharField(u"Css", max_length=360, default=u'')
    label = models.CharField(u"Ярлык", max_length=660, default='')

    total = models.PositiveIntegerField(u"Остаток", default=0)

    nomenclature = models.ForeignKey('sale.Nomenclature', null=True, blank=True, verbose_name=u'Номенклатура')

    order = ('begin','add','t_from','t_to','sold','m_from','m_to','m_rmv','inv','total')

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def get_absolute_url(self):
        return reverse('brick:Brick',kwargs=dict(id=self.pk))

    def make_label(self):
        return make_label(self)

    def make_css(self):
        return make_css(self)

    @property
    def mass(self):
        return mass[self.weight]

    class Meta():
        ordering = BrickOrder
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'
        permissions = (("view_brick", u"Может просматривать таблицу с остатками"),)

class OldBrick(Brick):
    old = models.IntegerField('Старое ID')
    prim = models.CharField(u"Имя", max_length=260, default='', help_text=u'Старое "имя"')
