# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from whs.brick.models import *
from whs.manufacture.models import *

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


@receiver(post_save, sender=Add)
def add_post_save(instance, *args, **kwargs):
    """
    Сигнал для производства.
    Создание изнемений в остатках
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total += instance.amount
    brick.save()
    print brick.total


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


@receiver(post_save, sender=Sorting)
def sorting_post_save(instance, *args, **kwargs):
    """
    Сигнал для "выдачи в цех"
    Создающий изменения
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()


@receiver(pre_delete, sender=Sorted)
@receiver(pre_save, sender=Sorted)
def sorted_pre_save(instance, *args, **kwargs):
    """
    Сигнал для выдачи в цеха сортированного кирпича.
    Убирает изменения от отперации
    """
    if instance.pk:
        origin = Sorted.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total -= origin.amount
        brick.save()


@receiver(post_save, sender=Sorted)
def sorted_post_save(instance, *args, **kwargs):
    """
    Сигнал для выдачи в цеха сортированного кирпича.
    Создаёт изменения от отперации
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total += instance.amount
    brick.save()


@receiver(pre_delete, sender=Removed)
@receiver(pre_save, sender=Removed)
def removed_pre_save(instance, *args, **kwargs):
    """
    Сигнал для списанного кирпича в процессе переборки
    Отменяет изменения от операции
    """
    if instance.pk:
        origin = Removed.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()


@receiver(post_save, sender=Removed)
def removed_post_save(instance, *args, **kwargs):
    """
    Сигнал для списанного кирпича в процессе переборки
    Создаёт изменение операции
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()


@receiver(pre_delete, sender=Write_off)
@receiver(pre_save, sender=Write_off)
def removed_pre_save(instance, *args, **kwargs):
    """
    Сигнал для списанного кирпича по итогам инвенторизации
    Отменяет изменения от операции
    """
    if instance.pk:
        origin = Write_off.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.save()


@receiver(post_save, sender=Write_off)
def removed_post_save(instance, *args, **kwargs):
    """
    Сигнал для списанного кирпича по итогам инвенторизации
    Создаёт изменение операции
    """
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.save()