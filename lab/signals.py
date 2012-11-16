# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from lab.models import *


@receiver(post_save, sender=Batch)
def batch_post_save(instance, *args, **kwargs):
    if instance.volume and instance.weight:
    	batch.density = round(batch.weight / batch.volume.volume,2)
		b.save()