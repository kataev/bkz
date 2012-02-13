# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from whs.bill.models import *
from whs.brick.models import *
from whs.manufacture.models import *

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
def sold_m2m(instance, pk_set, model, action, sender, *args, **kwargs):
    print action, pk_set
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


@receiver(pre_save, sender=Add)
@transaction.commit_on_success
def add_pre_save(instance, *args, **kwargs):
    if instance.pk:
        for h in History.objects.filter(date__gte=origin.doc.date.replace(day=1), brick=origin.brick).values('date',
            total=F('total') - origin.amount, begin=F('begin') - origin.amount,): # Проверка на отрицательные
            if h['total'] < 0:
                raise ValidationError(
                    'Остаток в месяце %s получится меньше 0, операция прервана' % h['date'])
            if h['begin'] < 0:
                raise ValidationError('Значение кирпича на начало месяца %s получится меньше 0, операция прервана' % h['date'])

        origin = Add.objects.get(pk=instance.pk) # Берём оригинальную операцию
        if History.objects.get(date=origin.doc.date.replace(day=1),
            brick=origin.brick).values(add=F('add') - origin.amount)['add'] < 0:
            raise ValidationError('Сколько кирпича в месяце %s не было!')

        brick = Brick.objects.get(pk=origin.brick.pk) # Кирпич этой операции (Уход од кеширования)
        brick.total -= origin.amount # Вычитаем остатки
        if origin.doc.date == datetime.date.today().replace(day=origin.doc.date.day): # Дата док-та этого месяца?
            brick.add -= origin.amount # Если да то просто вычетаем из прихода кол-во
        else:
            brick.begin -= origin.amount # Если нет вычитаем из начала т.к это влияет на предыдущие месяцы
            try:
                h = History.objects.get(date_gt=origin.doc.date, brick=origin.brick) # Запись в истории
                h.sold -= origin.amount # Вычитаем приход из того месяца
                h.save()
            except History.DoesNotExist: pass
            History.objects.filter(date__gte=origin.doc.date.replace(day=1), brick=origin.brick).update(
                total=F('total') - origin.amount) # И правим этот и остальные месяцы вычитая из остатков кол-во
            History.objects.filter(date__gt=origin.doc.date.replace(day=1), brick=origin.brick).update(
                begin=F('begin') - origin.amount) # Также вычитаем из последующих месяцев остатки на начало месяца
        brick.save()


@receiver(post_save, sender=Add)
@transaction.commit_on_success
def add_post_save(instance, *args, **kwargs):
    origin = Add.objects.get(pk=instance.pk) # Берём оригинальную операцию
    brick = Brick.objects.get(pk=origin.brick.pk) # Кирпич этой операции (Уход од кеширования)
    brick.total += origin.amount # Добавляем остатки
    if origin.doc.date == datetime.date.today().replace(day=origin.doc.date.day): # Дата док-та этого месяца?
        brick.add += origin.amount # Если да то просто добавляем в приход кол-во кирпича
    else:
        brick.begin += origin.amount # Если нет то добавляем в начало т.к это влияет на предыдущие месяцы
        try:
            h = History.objects.get(date_gt=origin.doc.date, brick=origin.brick) # Запись в истории
            h.sold += origin.amount # Добавляем приход из того месяца
            h.save()
        except History.DoesNotExist: pass
        History.objects.filter(date__gte=origin.doc.date.replace(day=1), brick=origin.brick).update(
            total=F('total') + origin.amount) # И правим этот и остальные месяцы вычитая из остатков кол-во
        History.objects.filter(date__gt=origin.doc.date.replace(day=1), brick=origin.brick).update(
            begin=F('begin') + origin.amount) # Также добавляем из последующих месяцев остатки на начало месяца
    brick.save()