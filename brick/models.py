# -*- coding: utf-8 -*-
from django.utils import datetime_safe as datetime
from django.db import models
from django.core.urlresolvers import reverse
from constants import *

class Brick(models.Model):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """

    cavitation = models.PositiveIntegerField(u"Пустотелость", choices=cavitation_c, default=cavitation_c[0][0])
    color = models.PositiveIntegerField(u"Цвет", choices=color_c, default=color_c[0][0])
    mark = models.PositiveIntegerField(u"Марка", choices=mark_c, default=mark_c[0][0])
    width = models.FloatField(u"Ширина", choices=width_c, default=width_c[0][0])
    view = models.CharField(u"Вид", max_length=60, choices=view_c, default=view_c[0][0])
    ctype = models.CharField(u"Тип цвета", max_length=6, choices=color_type_c, default=color_type_c[0][0],blank=True)
    defect = models.CharField(u"Брак в %", max_length=60, choices=defect_c, default=defect_c[0][0],blank=True)
    refuse = models.CharField(u"Особенности", max_length=10, choices=refuse_c, default=refuse_c[0][0],blank=True)
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
        return reverse('brick:Brick-view',kwargs=dict(id=self.pk))

    def make_label(self):
        return make_label(self)

    def make_css(self):
        return make_css(self)

    @property
    def mass(self):
        return mass_c[self.width]

    class Meta():
        ordering = BrickOrder
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'
        permissions = (("view_brick", u"Может просматривать таблицу с остатками"),)

class OldBrick(Brick):
    old = models.IntegerField('Старое ID')
    prim = models.CharField(u"Имя", max_length=260, default='', help_text=u'Старое "имя"')
