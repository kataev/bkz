# -*- coding: utf-8 -*-
from old.models import *
#from brick.models import *
import re

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


def fetch_brick():
    tovar = Tovar.objects.using('old').all().order_by('id')
#    bricks = map(lambda x: x[0],Brick.objects.values_list('pk').order_by('id'))
    for b in tovar:
        prim = b.prim
        mark =  re.search('100|125|150|175|200 |250',prim)
        if mark: mark = int(mark.group())
        else: mark = 9000
        cl = re.search('КЕ',prim)
        if cl:
            cl = 6
        else:
            cl = re.search('Желтый|Коричневый',prim)
            if cl:
                cl = cl.group()
        print cl

