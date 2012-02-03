# -*- coding: utf-8 -*-
from django.db import models
from constants import *

class Brick(models.Model):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """

    color = models.PositiveIntegerField(u"Цвет", choices=color)
    mark = models.PositiveIntegerField(u"Марка",choices=mark)
    weight = models.FloatField(u"Ширина",choices=weight)
    view = models.CharField(u"Вид",max_length=60, choices=view)
    ctype = models.CharField(u"Тип цвета",max_length=6,choices=color_type,blank=True)
    defect = models.CharField(u"Брак в %",max_length=60,choices=defect,blank=True)
    refuse = models.CharField(u"Особенности",max_length=10,choices=refuse,blank=True)
    features = models.CharField(u"Редкие особенности",max_length=60,blank=True,help_text=u'Oттенки, тычки и прочее')
    name = models.CharField(u"Имя",max_length=160,default='')
    total = models.PositiveIntegerField(u"Остаток",default=0)

    css=models.CharField(u"Css",max_length=360,default=u'')
    label=models.CharField(u"Имя",max_length=660,default='')

    begin = models.PositiveIntegerField(u"Начало месяца",default=0)
    add = models.PositiveIntegerField(u"Приход",default=0)
    t_from = models.PositiveIntegerField(u"Перевод из",default=0)
    t_to = models.PositiveIntegerField(u"Перевод в",default=0)
    sold = models.PositiveIntegerField(u"Отгрузка",default=0)

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def get_absolute_url(self):
        return "/brick/%i/" % self.id

    class Meta():
        ordering=['-weight','color','-view','ctype','defect','refuse','mark','features',]
        verbose_name = u"кирпич"
        verbose_name_plural = u'кирпичи'


class History(models.Model):
    brick = models.ForeignKey(Brick,related_name="%(app_label)s_%(class)s_related",verbose_name=u'Кирпич')
    date = models.DateField()

    begin = models.PositiveIntegerField(u"Начало месяца")
    add = models.PositiveIntegerField(u"Приход")
    t_from = models.PositiveIntegerField(u"Перевод из")
    t_to = models.PositiveIntegerField(u"Перевод в")
    sold = models.PositiveIntegerField(u"Отгрузка")
    total = models.PositiveIntegerField(u"Остаток")