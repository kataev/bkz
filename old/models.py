# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class DispAgent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    inn = models.TextField()
    address = models.TextField()
    schet = models.TextField()
    bank = models.TextField()
    phone = models.TextField()
    cp = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'agent'
        

class DispJurnal(models.Model):
    id = models.IntegerField(primary_key=True)
    tov = models.ForeignKey('DispTovar',db_column='tov',verbose_name=u'Товар')
    plus = models.IntegerField(u'Приход')
    minus = models.IntegerField(u'Отгрузка')
    poddon = models.IntegerField(u'Кол-во поддонов')
    agent = models.ForeignKey('DispAgent',db_column='agent',verbose_name=u'Контрагент')
    akt = models.IntegerField(u'Номер акта при переводе')
    nakl = models.TextField(u'Номер накладной')
    makt = models.IntegerField(u'Перевод из')
    pakt = models.IntegerField(u'Перевод в')
    spis = models.IntegerField(u'Списание')
    no_con = models.IntegerField(u'Не кнодиция')
    workshop = models.IntegerField(u'После сортировки')
    mws = models.IntegerField(u'В сортировку')
    date = models.DateField(u'Дата')
    time = models.DateTimeField(u'Время создания')
    prim = models.TextField(u'Примичание')
    money = models.FloatField(u'Деньги при продаже')
    price = models.FloatField(u'Цена за кирпич')
    trans = models.FloatField(u'Доставка')

    def __unicode__(self):
        if self.minus:
            return u'minus %d' % self.minus
        elif self.plus:
            return u'plus %d' % self.plus
        elif self.akt:
            return u'akt %d' % self.akt
        elif self.spis:
            return u'spis %d' % self.spis
        elif self.no_con:
            return u'no_con %d' % self.no_con
        elif self.workshop:
            return u'workshop %d' % self.workshop
        else:
            return u'x3'
    def m(self):
        return self.price * self.minus

    class Meta:
        db_table = u'jurnal'
        ordering = ('-date',)

class DispSclad(models.Model):
    id = models.IntegerField(primary_key=True)
    total = models.IntegerField()

    def __unicode__(self):
        return str(self.total)

    class Meta:
        db_table = u'sclad'

class DispTovar(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    mark = models.IntegerField()
    color = models.TextField()
    tip = models.IntegerField()
    vid = models.TextField()
    mas = models.TextField()
    brak = models.TextField()
    prim = models.TextField()
    sort = models.IntegerField()
    price = models.IntegerField()
    total = models.ForeignKey('DispSclad',db_column='id')

    def __unicode__(self):
        return self.prim

    class Meta:
        db_table = u'tovar'
        ordering = ('id',)

