# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from whs.bill.models import *

@receiver(pre_delete, sender=Sold)
@receiver(pre_save, sender=Sold)
def sold_pre_save(instance, *args, **kwargs):
    print 'test'
    if instance.pk:
        instance = Sold.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total += instance.amount
        brick.save()

@receiver(post_save, sender=Sold)
def sold_post_save(instance, *args, **kwargs):
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()

@receiver(pre_delete, sender=Transfer)
@receiver(pre_save, sender=Transfer)
def transfer_pre_save(instance, *args, **kwargs):
    if instance.pk:
        instance = Transfer.objects.get(pk=instance.pk)
        brick_from = Brick.objects.get(pk=instance.brick_from.pk)
        brick_from.total += instance.amount
        brick_from.save()

@receiver(post_save, sender=Transfer)
def transfer_post_save(instance, *args, **kwargs):
    brick_from = Brick.objects.get(pk=instance.brick_from.pk)
    brick_from.total -= instance.amount
    brick_from.save()
