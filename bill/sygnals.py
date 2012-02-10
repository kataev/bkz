# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from whs.bill.models import *

@receiver(pre_save,sender=Sold)
def sold_pre_save(instance,*args,**kwargs):
    if instance.pk:
        origin = Sold.objects.get(pk=instance.pk)
        origin.brick.total+=origin.amount
        origin.brick.sold-=origin.amount
        origin.brick.save()

@receiver(post_save,sender=Sold)
def sold_post_save(instance,*args,**kwargs):

    instance.brick.total-=instance.amount
    instance.brick.sold+=instance.amount
    instance.brick.save()


@receiver(post_save,sender=Sold)
def money(instance,*args,**kwargs):
    """ Сигнал для обновления информации о кол-ве бабла. """
    instance.money = sum(map(lambda x: x['amount']*x['price'], instance.bill_sold_related.values('amount','price')))
    instance.save()
  