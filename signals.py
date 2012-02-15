# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from django.db import transaction,IntegrityError
from django.db.models import F
from django.core.exceptions import ValidationError

from whs.bill.models import *
from whs.brick.models import *
from whs.manufacture.models import *

#@receiver(pre_delete, sender=Sold)
#@receiver(pre_save, sender=Sold)
#def sold_pre_save(instance, *args, **kwargs):
#    if instance.pk:
#        origin = Sold.objects.get(pk=instance.pk)
#        brick = Brick.objects.get(pk=origin.brick.pk)
#        brick.total += origin.amount
#        brick.save()
#
#@receiver(post_save, sender=Sold)
#def sold_post_save(instance, *args, **kwargs):
#    brick = Brick.objects.get(pk=instance.brick.pk)
#    brick.total -= instance.amount
#    brick.save()
#
@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def transfer_pre_save(instance, model, *args, **kwargs):
    if instance.sold.get():
        origin = model.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()

@receiver(post_save, sender=Add)
def transfer_post_save(instance, *args, **kwargs):
    if instance.sold.get():
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total -= instance.amount
        brick.save()

@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def add_pre_save(instance,model, *args, **kwargs):
    if instance.pk:
        origin = Add.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total -= origin.amount
        brick.save()

@receiver(post_save, sender=Add)
def add_post_save(instance, *args, **kwargs):
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total += instance.amount
    brick.save()