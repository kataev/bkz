# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from whs.brick.models import *
from whs.manufacture.models import *

@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def add_pre_save(instance, *args, **kwargs):
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