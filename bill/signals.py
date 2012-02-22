# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from whs.brick.models import *
from whs.bill.models import *

@receiver(pre_delete, sender=Sold)
@receiver(pre_save, sender=Sold)
def sold_pre_save(instance, *args, **kwargs):
    if instance.pk:
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total += instance.amount
        brick.save()

@receiver(post_save, sender=Sold)
def sold_post_save(instance, *args, **kwargs):
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()