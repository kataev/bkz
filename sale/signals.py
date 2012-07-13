# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from bkz.sale.models import *

@receiver(pre_delete, sender=Sold)
@receiver(pre_save, sender=Sold)
def sold_pre_save(instance, *args, **kwargs):
    if instance.pk:
        instance = Sold.objects.get(pk=instance.pk)
        if instance.brick_from:
            brick = Brick.objects.get(pk=instance.brick_from_id)
        else:
            brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total += instance.amount
        brick.save()

@receiver(post_save, sender=Sold)
def sold_post_save(instance, *args, **kwargs):
    if instance.brick_from:
        brick = Brick.objects.get(pk=instance.brick_from_id)
    else:
        brick = Brick.objects.get(pk=instance.brick_id)
    brick.total -= instance.amount
    brick.save()