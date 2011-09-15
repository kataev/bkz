# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

class Agent(models.Model):

    type_c = ((0,u'Обычный покупатель'),(1,u'Строительная компания'))

    name=models.CharField(u"Имя",max_length=200)
    form=models.CharField(u"Юр форма",blank=True,max_length=200)
    type=models.IntegerField(u'Тип',choices=type_c,help_text=u'Выберите тип контрагента',default=0)
    address=models.CharField(u"Адресс",blank=True,max_length=200)
    bank=models.CharField(u"Банк",blank=True,max_length=200)
    phone=models.CharField(u"Телефон",blank=True,max_length=200)
    inn=models.CharField(u"Инн",blank=True,max_length=200)
    account=models.CharField(u"Счет",blank=True,max_length=200)

    def bills(self):
        return u'/bill/?agent=%s' % self.id

    def cool_name(self):
        name = self.name.split(' ')
        if len(name) == 3 and self.form != u'ООО':
            return u'%s %1s.%1s' % (name[0],name[1][:1],name[2][:1])
        else:
            return self.name


    class Meta:
        verbose_name=u'Контрагент'
        verbose_name_plural=u'Контрагенты'

    def __unicode__(self):
        if self.pk:
            return u'%s, %s' % (self.name,self.form)
        else:
            return u'Новый контрагент'

admin.site.register(Agent)