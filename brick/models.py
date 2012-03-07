# -*- coding: utf-8 -*-
from django.db import models
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

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def get_absolute_url(self):
        return u"/%s/%i/" % (self._meta.verbose_name,self.id)

    def make_label(self):
        return make_label(self)

    def make_css(self):
        return make_css(self)

    class Meta():
        ordering = BrickOrder
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'
        permissions = (("view_brick", u"Может просматривать таблицу с остатками"),)


#class History(models.Model):
#    brick = models.ForeignKey(Brick, related_name="%(app_label)s_%(class)s_related", verbose_name=u'Кирпич')
#    date = models.DateField()
#
#    begin = models.PositiveIntegerField(u"Начало месяца")
#    add = models.PositiveIntegerField(u"Приход")
#    t_from = models.PositiveIntegerField(u"Перевод из")
#    t_to = models.PositiveIntegerField(u"Перевод в")
#    sold = models.PositiveIntegerField(u"Отгрузка")
#    total = models.PositiveIntegerField(u"Остаток")
#
#    class Meta:
#        verbose_name = u'Архив'


