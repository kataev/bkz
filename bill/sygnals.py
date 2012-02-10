# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from whs.bill.models import *

@receiver(post_save,sender=Sold)
def money(*args,**kwargs):
    kwargs['instance'].doc.set_money()
  