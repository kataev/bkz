# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver

from whs.brick.models import *
from whs.bill.models import *

@receiver(pre_delete, sender=Sold)
@receiver(pre_save, sender=Sold)
def sold_pre_save(instance, *args, **kwargs):
    if instance.pk and not instance.transfered:
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total += instance.amount
        brick.save()

@receiver(post_save, sender=Sold)
def sold_post_save(instance, *args, **kwargs):
    if not instance.transfered:
        brick = Brick.objects.get(pk=instance.brick.pk)
        brick.total -= instance.amount
        brick.save()

@receiver(m2m_changed, sender=Sold.transfer.through)
def sold_m2m(instance,pk_set,model,action,sender,*args, **kwargs):
    print action
    if action == 'pre_clear':
        for t in instance.transfer.all():
            b = Brick.objects.get(pk=t.brick.pk)
            b.total += t.amount
            b.save()
    if action == 'post_add':
        if instance.amount == instance.transfer_amount:
            for t in instance.transfer.all():
                b = Brick.objects.get(pk=t.brick.pk)
                b.total -= t.amount
                b.save()