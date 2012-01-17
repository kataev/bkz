# -*- coding: utf-8 -*-
from django.db import models
from constants import *
from django.db.models import Q

class Brick(models.Model):
    """ Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке """

    color=models.CharField(u"Цвет",max_length=60, choices=color_c)
    mark=models.PositiveIntegerField(u"Марка",choices=mark_c)
    weight=models.CharField(u"Ширина",max_length=60, choices=weight_c)
    view=models.CharField(u"Вид",max_length=60, choices=view_c)
    color_type=models.CharField(u"Тип цвета",max_length=6,choices=color_type_c,blank=True)
    defect=models.CharField(u"Брак в %",max_length=60,choices=defect_c,blank=True)
    refuse=models.CharField(u"Особенности",max_length=10,choices=refuse_c,blank=True)
    features=models.CharField(u"Редкие особенности",max_length=60,blank=True,help_text=u'Oттенки, тычки и прочее')
    name=models.CharField(u"Имя",max_length=160,default='')
    total=models.PositiveIntegerField(u"Текуший остаток",default=0)

    css=models.CharField(u"Css",max_length=360,default=u'')
    label=models.CharField(u"ИмяЯ",max_length=660,default='')

    def __unicode__(self):
        if not self.pk: return u'Новый кирпич'
        else: return self.label

    def get_absolute_url(self):
        return "/brick/%i/" % self.id

    class Meta():
        ordering=['color','-weight','-view','color_type','defect','refuse','mark','features',]
        verbose_name = u"кирпич"
        verbose_name_plural = u'кирпичи'

    css_dict= dict(
        color=[u'red',u'yellow',u'brown',u'light',u'white'],
        weight={u'1': u'single', u'1.4': u'thickened', u'2': u'double', u'EU':u'euro'},
        view={u'Л': u'facial', u'Р': u'common'},
        color_type={'': u'type0', '1': u"type1", '2': u'type2', '3': u'type3'},
        defect={u'': u'lux', u'<20': u'p_20', u'>20': u'm_20'})

class BrickTable(Brick):
    """ Абстракная модель, наследованая от кирпича. Не содержит данных,
    Необходима для представления, чтобы на нее навешивать данные
    посчитанные при обработке запроса. """
    
    begin=models.PositiveIntegerField(u"Начало месяца",default=0)
    add=models.PositiveIntegerField(u"Приход",default=0)
    t_from=models.PositiveIntegerField(u"Перевод из",default=0)
    t_to=models.PositiveIntegerField(u"Перевод в",default=0)
    sold=models.PositiveIntegerField(u"Отгрузка",default=0)

    class Meta:
        abstract = True

class OldBrick(Brick):
    old_id= models.IntegerField('old id')