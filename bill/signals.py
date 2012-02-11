# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from whs.bill.models import *
from django.db import transaction

@receiver(pre_save, sender=Sold)
def sold_pre_save(instance, *args, **kwargs):
    if instance.pk:
        origin = Sold.objects.get(pk=instance.pk)
        brick = Brick.objects.get(pk=origin.brick.pk)
        brick.total += origin.amount
        brick.sold -= origin.amount
        brick.save()

@receiver(post_save, sender=Sold)
def sold_post_save(instance, *args, **kwargs):
    brick = Brick.objects.get(pk=instance.brick.pk)
    brick.total -= instance.amount
    brick.sold += instance.amount
    brick.save()

@receiver(post_save, sender=Sold)
def money(instance, *args, **kwargs):
    """ Сигнал для обновления информации о кол-ве бабла. """
    instance.doc.money = sum(
        map(lambda x: x['amount'] * x['price'], instance.doc.bill_sold_related.values('amount', 'price')))
    instance.doc.save()


@receiver(m2m_changed, sender=Sold.transfer.through)
@transaction.commit_on_success
def sold_m2m(instance,pk_set,model,action,sender,*args, **kwargs):
    print action,pk_set
    if action == 'pre_add':
        for id in pk_set:
            s = instance
            t = model.objects.get(pk=id)
            sb = Brick.objects.get(pk=s.brick.pk)
            tb = Brick.objects.get(pk=t.brick.pk)
            sb.total += t.amount
            sb.t_to += t.amount

            tb.total -= t.amount
            tb.t_from += t.amount

            sb.save()
            tb.save()

    if action == "pre_clear":

        for t in instance.transfer.all():
            s = instance
            sb = Brick.objects.get(pk=s.brick.pk)
            tb = Brick.objects.get(pk=t.brick.pk)

            sb.total -= t.amount
            sb.t_to -= t.amount

            tb.total += t.amount
            tb.t_from -= t.amount

            sb.save()
            tb.save()