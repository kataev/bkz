# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from django.db import transaction, IntegrityError,connection
from django.db.models import F

from whs.bill.models import *
from whs.brick.models import *
from whs.manufacture.models import *

#@receiver(post_save, sender=Brick)
def brick_order(instance, *args, **kwargs):
    cursor = connection.cursor()
    cursor.execute('REINDEX INDEX "brick_brick_order";')

@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def add_pre_save(instance, model, *args, **kwargs):
    if instance.sold.get():
        origin = model.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()

@receiver(post_save, sender=Add)
def add_post_save(instance, *args, **kwargs):
    if instance.sold.get():
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total -= instance.amount
        brick.save()

@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def add_pre_save(instance, model, *args, **kwargs):
    if instance.pk:
        origin = Add.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()

@receiver(post_save, sender=Add)
def add_post_save(instance, *args, **kwargs):
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total += instance.amount
    brick.save()