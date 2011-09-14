# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from whs.bill.models import Doc,Oper

class Inc(Oper):
    class Meta():
        verbose_name = u"Приход"
        verbose_name_plural = u"Приходы"

class Gain(Doc):
    incoming = models.ManyToManyField(Inc,related_name="%(app_label)s_%(class)s_related",
                                      blank=True,null=True,
                                      help_text=u'Отгрузки',
                                      verbose_name=u'Приход')
    class Meta():
        verbose_name = u"Приход с производства за день"
        verbose_name_plural = u"Приход с производства за день"



admin.site.register(Inc)
admin.site.register(Gain)
