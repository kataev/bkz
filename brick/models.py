# -*- coding: utf-8 -*-
from django.db import models
from constants import *

class Brick(models.Model):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """

    def __init__(self,*args,**kwargs):
        super(Brick,self).__init__(*args,**kwargs)
#        self.get_view_display = self.get_view_display_replace


    color = models.PositiveIntegerField(u"Цвет", choices=color)
    mark = models.PositiveIntegerField(u"Марка",choices=mark)
    weight = models.FloatField(u"Ширина",choices=weight)
    view = models.CharField(u"Вид",max_length=60, choices=view)
    color_type = models.CharField(u"Тип цвета",max_length=6,choices=color_type,blank=True)
    defect = models.CharField(u"Брак в %",max_length=60,choices=defect,blank=True)
    refuse = models.CharField(u"Особенности",max_length=10,choices=refuse,blank=True)
    features = models.CharField(u"Редкие особенности",max_length=60,blank=True,help_text=u'Oттенки, тычки и прочее')
    name = models.CharField(u"Имя",max_length=160,default='')
    total = models.PositiveIntegerField(u"Текуший остаток",default=0)

    css=models.CharField(u"Css",max_length=360,default=u'')
    label=models.CharField(u"ИмяЯ",max_length=660,default='')

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def get_absolute_url(self):
        return "/brick/%i/" % self.id

    def get_view_display_replace(self):
        if self.weight == 0.8:
            if self.view == u'Л':
                return u'УЛ'
            else:
                return u''
        else:
            return self._get_FIELD_display(self._meta.get_field('view'))

    class Meta():
        ordering=['color','-weight','-view','color_type','defect','refuse','mark','features',]
        verbose_name = u"кирпич"
        verbose_name_plural = u'кирпичи'


class BrickTable(Brick):
    """ Абстракная модель, наследованая от кирпича. Не содержит данных,
    Необходима для представления, чтобы на нее навешивать данные
    посчитанные при обработке запроса. """
    
    begin = models.PositiveIntegerField(u"Начало месяца",default=0)
    add = models.PositiveIntegerField(u"Приход",default=0)
    t_from = models.PositiveIntegerField(u"Перевод из",default=0)
    t_to = models.PositiveIntegerField(u"Перевод в",default=0)
    sold = models.PositiveIntegerField(u"Отгрузка",default=0)

    class Meta:
        abstract = True

class OldBrick(Brick):
    old_id = models.IntegerField('old id')