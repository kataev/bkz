# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
type_c = ((0,u'Обычный покупатель'),(1,u'Строительная компания'))
#form_c = ((0,u'Обычный покупатель'),(1,u'Строительная компания'))

class Agent(models.Model):
    name=models.CharField(u"Имя",max_length=200,help_text=u'Название без юридической формы')
    form=models.CharField(u"Юр форма",blank=True,max_length=200,help_text=u'Юридическая форма, ООО,ОАО и т.д')
    type=models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)
    address=models.CharField(u"Адрес",blank=True,max_length=200,help_text=u'Юридический адрес')
    bank=models.CharField(u"Банк",blank=True,max_length=200)
    phone=models.CharField(u"Телефон",blank=True,max_length=200)
    inn=models.CharField(u"Инн",blank=True,max_length=200)
    okpo=models.IntegerField(u'ОКПО',help_text=u'Введите код ОКПО',default=0)
    account=models.CharField(u"Расчетный счет",blank=True,max_length=200)
    account_ks=models.CharField(u"Корректиционный счет",blank=True,max_length=200)

    class Meta:
        verbose_name=u'Контрагент'
        verbose_name_plural=u'Контрагенты'
        permissions = (("view_agent", u"Может просматривать контрагентa"),)
        ordering = ('name', )

    def __unicode__(self):
        if self.pk:
            name = self.name.split(' ')
            if len(name) == 3 and self.form != u'ООО':
                return u'%s %1s.%1s' % (name[0],name[1][:1],name[2][:1])
            else:
                return self.name[:30]
        else:
            return u'Новый контрагент'

    def get_absolute_url(self):
        return u"/%s/%i/" % (self._meta.verbose_name,self.id)