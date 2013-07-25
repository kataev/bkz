# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver

from lab.models import Batch, Part


@receiver(post_save, sender=Batch)
def batch_post_save(instance, *args, **kwargs):
    if instance.volume and instance.weight:
        instance.density = round(instance.weight / instance.volume.volume, 2)
        instance.save()


@receiver(post_save, sender=Part)
def part_post_save(instance, *args, **kwargs):
    tto = instance.get_tto
    print tto
