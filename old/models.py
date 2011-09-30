# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Agent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    inn = models.TextField()
    address = models.TextField()
    schet = models.TextField()
    bank = models.TextField()
    phone = models.TextField()
    cp = models.IntegerField()
    class Meta:
        db_table = u'agent'
        

class Jurnal(models.Model):
    id = models.IntegerField(primary_key=True)
    tov = models.IntegerField()
    plus = models.IntegerField()
    minus = models.IntegerField()
    poddon = models.IntegerField()
    agent = models.IntegerField()
    akt = models.IntegerField()
    nakl = models.TextField()
    makt = models.IntegerField()
    pakt = models.IntegerField()
    spis = models.IntegerField()
    no_con = models.IntegerField()
    workshop = models.IntegerField()
    mws = models.IntegerField()
    date = models.DateField()
    time = models.DateTimeField()
    prim = models.TextField()
    money = models.FloatField()
    price = models.FloatField()
    trans = models.FloatField()
    class Meta:
        db_table = u'jurnal'

class Sclad(models.Model):
    id = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    class Meta:
        db_table = u'sclad'

class Tovar(models.Model):
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
#    total = models.ForeignKey(Sclad)


    class Meta:
        db_table = u'tovar'

