# -*- coding: utf-8 -*-
from whs.old.models import Agent as Aold
from whs.brick.models import OldBrick
from whs.old.models import Tovar,Jurnal,Sclad
from whs.agent.models import Agent
from whs.bill.models import *
import re
from django.http import HttpResponse
import datetime

view_c=((u'Л',u'Лицевой'),(u'Р',u'Рядовой'))
weight_c=((u'1',u'Одинарный'),(u'1.4',u'Утолщенный'),(u'2',u'Двойной'))
color_c=((u'Кр',u'Красный'),
               (u'Же',u'Желтый'),
               (u'Ко',u'Коричневый'),
               (u'Св',u'Светлый'),
               (u'Бе',u'Белый'))

class_c=((0,u'Красный'),
               (1,u'Желтый'),
               (2,u'Коричневый'),
               (3,u'Светлый'),
               (4,u'Белый'),
               (5,u'Евро'),
               (6,u'Прочее'))

mark_c=((100,u'100'),
        (125,u'125'),
        (150,u'150'),
        (175,u'175'),
        (200,u'200'),
        (250,u'250'),
        (9000,u'брак'))

def fetch_brick(request):
    """
    Доставание кирпича, просто мрак!
    """
    tovar = Tovar.objects.using('old').all().order_by('id')
    responce = u''
    for b in tovar:
        prim = b.prim
        mark =  re.search('100|125|150|175|200 |250',prim)
        if mark: mark = int(mark.group())
        else: mark = 9000
#        print prim
        cl = re.search(u'КЕ',prim,re.U)
        if cl:
            cl = 5
            if re.search(u'УЛ',prim,re.U):
                view = u'Л'
            else:
                view = u'Р'
            weight = u'1'
        else:
            cl = re.search(u'желтый|корич|светлый|белый',prim,re.U)
            if cl:
                cl = cl.group()
                for c in class_c:
                    if unicode(cl) in c[1].lower():
                        cl = c[0]
            else:
                cl = 0
            if re.search(u'ЛПу',prim,re.U):
                view = u'Л'
            else:
                view = u'Р'
            if re.search(u'КО',prim,re.U):
                weight = u'1'
            else:
                weight = u'1.4'
        responce+='<div>%s | %s | %s | %s</div>' % (b.prim,cl,class_c[cl][1],view)
        try: OldBrick.objects.get(old_id=b.id)
        except OldBrick.DoesNotExist:
            bri = OldBrick(mark=mark,brick_class=cl,color=u'Кр',view=view,weight=weight,name=b.prim,css='1',label='1',old_id=b.id)
            bri.full_clean()
            bri.save()
    return HttpResponse(responce)

def fetch_total(request):
    """
    Актуализировать остатки кирпичей.
    """
    delete = ''
    for b in OldBrick.objects.all():
        try: b.total = Sclad.objects.using('old').get(pk=b.old_id).total
        except Sclad.DoesNotExist:
            print b.pk,b.old_id
            if not Jurnal.objects.using('old').filter(tov=b.old_id).count():
                delete+=' deleted %d' % b.pk
                b.delete()
        b.save()
    return HttpResponse('FINISH %s' %delete)

def agents():
    """
    Перенос агентов
    """
    agent = Aold.objects.using('old').all().order_by('id')
    for a in agent:
        Agent(pk=a.id,name=a.name).save()
    return HttpResponse('FINISH')

def fetch_transfer(request):
    """
    Перенос переводов с угадыванием точки получения
    """
    a = {}
    for j in Jurnal.objects.using('old').filter(pakt__gt=0):
        if j.date:
            s = Sold.objects.filter(doc__date__month=j.date.month, doc__date__year=j.date.year,
                                    amount__gte=j.pakt,brick=OldBrick.objects.get(old_id=j.tov))
            if s:
                a[j.akt] = s[0]
    print 'finish sold',a
    for j in Jurnal.objects.using('old').filter(makt__gt=0):
        if a.get(j.akt):
            t = Transfer(brick=OldBrick.objects.get(old_id=j.tov),
                         amount=j.makt,sold=a[j.akt],doc=a[j.akt].doc)
            t.save()
    return HttpResponse('FINISH')

def fetch_oper(request):
    """
    Достать продажи из старой базы и положить в новую.
    """
    i = 99990
    for j in Jurnal.objects.using('old').filter(minus__gt=0).order_by('id'):
        try:nakl = int(j.nakl)
        except ValueError:
                nakl = i
                i+=1
                print j.nakl,j.pk
        try: bill = Bill.objects.get(number=nakl,date=j.date)
        except Bill.DoesNotExist:
            bill = Bill(number=nakl,date=j.date,agent=Agent.objects.get(pk=j.agent),info=j.prim)
            bill.save()
        s = Sold(brick=OldBrick.objects.get(old_id=j.tov),
                 amount=j.minus,doc=bill,price=j.price,delivery=j.trans)
        s.save()
    return HttpResponse('FINISH')