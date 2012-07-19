# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from whs.models import *

#@receiver(post_save,sender=Brick)
#def brick_make(instance, *args, **kwargs):


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


@receiver(post_save, sender=Add)
def add_post_save(instance, *args, **kwargs):
    """
    Сигнал для производства.
    Создание изнемений в остатках
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total += instance.amount
    brick.save()


@receiver(pre_delete, sender=Add)
@receiver(pre_save, sender=Add)
def add_pre_save(instance, *args, **kwargs):
    """
    Сигнал для производства.
    Убирает изменения операции на остатки
    """
    if instance.pk:
        origin = Add.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total -= origin.amount
        brick.save()


@receiver(post_save, sender=Sorting)
def sorting_post_save(instance, *args, **kwargs):
    """
    Сигнал для "выдачи в цех"
    Создающий изменения
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()


@receiver(pre_delete, sender=Sorting)
@receiver(pre_save, sender=Sorting)
def sorting_pre_save(instance, *args, **kwargs):
    """
    Сигнал для "выдачи в цех"
    Отменяющий изменения
    """
    if instance.pk:
        origin = Sorting.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()