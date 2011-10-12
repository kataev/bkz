# -*- coding: utf-8 -*-
from whs.bill.models import Oper,Doc
from django.db import models
from django.contrib import admin


class Man(Doc):
    """Класс документа для учета прихода кирпича с производства"""
    class Meta():
            verbose_name = u"производство за день"

class Add(Oper):
    """Класс операций для документа"""
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)