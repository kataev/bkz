# -*- coding: utf-8 -*-
from whs.bill.models import Oper,Doc
from django.db import models
from django.contrib import admin


class Man(Doc):
    class Meta():
            verbose_name = u"производство за день"

class Add(Oper):
    doc = models.ForeignKey(Man,blank=False,related_name="%(app_label)s_%(class)s_related",null=False)