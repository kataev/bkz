# -*- coding: utf-8 -*-
from whs.old.models import Agent as Aold
from whs.brick.models import OldBrick
from whs.old.models import Tovar,Jurnal,Sclad
from whs.agent.models import Agent
from whs.bill.models import *
import re
from django.http import HttpResponse

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


type_c=(('',''),('1','1 тип'),('2','2 тип'),('3','3 тип'))
defect_c=((u'',u''),(u'<20',u'До 20%'),(u'>20',u'Более 20%'))
refuse_c=((u'',u''),(u'Ф',u'Фаска'),(u'ФП',u'Фаска Полосы'),(u'ФФ',u'Фаска Фаска'),(u'ФФП',u'Фаска Фаска Полосы'),(u'П',u'Полосы'))

def fetch_brick(request):
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
    for s in  Sclad.objects.using('old').all().order_by('id'):
        try: br = OldBrick.objects.get(old_id=s.id)
        except OldBrick.DoesNotExist: pass
        if br:
            br.total = s.total
            br.save()
    return HttpResponse()

def agents():
    agent = Aold.objects.using('old').all().order_by('id')
    for a in agent:
        Agent(pk=a.id,name=a.name).save()

def fetch_oper(request):
    responce = u''
    i = 99990
    for j in Jurnal.objects.using('old').filter(pk__gt=2000).order_by('id'):
        if j.minus:
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


    return HttpResponse(responce)