# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

type_c = ((0,u'Юр.Лицо'),(1,u'Физ.лицо'))

class Agent(models.Model):
    name = models.CharField(u"Имя",max_length=400,
        help_text=u'Название без юридической формы, без ООО, без ИП, без кавычек.')
    fullname = models.CharField(u"Полное имя",max_length=400,help_text=u'Название для накладных')
    type = models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)

    address = models.CharField(u"Адрес",blank=True,max_length=200,help_text=u'Юридический адрес')
    phone = models.CharField(u"Телефон",blank=True,max_length=200)

    inn = models.CharField(u"Инн",blank=True,max_length=200)
    kpp = models.CharField(u'КПП',help_text=u'Введите код ОКПО',blank=True,max_length=200)

    bank = models.CharField(u"Банк",blank=True,max_length=200)
    ks = models.CharField(u"Корректиционный счет",blank=True,max_length=200)
    bic = models.CharField(u"Бик",blank=True,max_length=200)

    rs=models.CharField(u"Расчетный счет",blank=True,max_length=200)

    class Meta:
        verbose_name=u'Контрагент'
        verbose_name_plural=u'Контрагенты'
        permissions = (("view_agent", u"Может просматривать контрагентa"),)
        ordering = ('name', )

    def __unicode__(self):
        if self.pk:
            return self.name[:40]
        else:
            return u'Новый контрагент'

    def get_absolute_url(self):
        return u"/%s/%i/" % (self._meta.verbose_name,self.id)

class Seller(Agent):
    class Meta:
        verbose_name=u'Продавец'
        verbose_name_plural=u'Продавецы'

        ordering = ('name', )

