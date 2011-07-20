# -*- coding: utf-8 -*-
import MySQLdb
from whs.bills.models import *
from whs.agents.models import *
from whs.bricks.models import *

def FetchOneAssoc(cursor) :
    data = cursor.fetchall()
    if data == None :
        return None
    desc = cursor.description

    d = []
    print len(data)
    for row in data:

        dict = {}
        for (name, value) in zip(desc, row) :
            dict[name[0]] = value
#        print dict['name']
        d.append(dict)

    return d

def check():
    db= MySQLdb.connect('localhost','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from sclad,tovar where sclad.id=tovar.id order by sclad.id;")
    data = FetchOneAssoc(cursor)
    a = {}
    b = {}

    for q in data:
        b['b'+str(q['id'])]=q


    for w in bricks.objects.all():
        try:
            del(b['b'+str(w.pk)])

        except KeyError,e:
            print w.pk,e
            w.delete()


    print b






def total_update():
    db= MySQLdb.connect('localhost','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from sclad,tovar where sclad.id=tovar.id order by sclad.id;")
    data = FetchOneAssoc(cursor)
    for r in data:
        try:
            b = bricks.objects.get(pk=int(r['id']))
        except b.DoesNotExist:
            view={u'Строительный':u'Р',u'Лицевой':u'Л'}
            weight={u'Полуторный':u'1.4',u'Двойной':u'2',u'Одинарный':u'1',u'Прочее':u'2'}
            class_c = {u'Красный':0,u'Желтый':1,u'Коричневый':2,u'Светлый':3,u'Белый':4,u'КЕ':5,u'Прочее':6}
            color = {u'Красный':u'Кр',u'Желтый':u'Же',u'Коричневый':u'Ко',u'Светлый':u'Св',u'Белый':u'Бе',u'КЕ':u'Кр',u'Прочее':u'Кр'}
#            print r
            if r['mark']==0:
                mark=9000
            else:
                mark=r['mark']
            brak=u''
            refuse=u''
            for w in r['brak']:
                if w==u'Меньше 20%':
                    brak = u'<20'
                if w==u'Больше 20%':
                    brak = u'>20'
                if w==u'Фаска':
                    refuse=u'Ф'
                if w==u'Полосы':
                    refuse=u'П'
#            print r['mas']
            b = bricks(pk=r['id'],brick_class=class_c[r['color']],
                       color=color[r['color']],
                       mark=mark,
                       weight=weight[r['mas']],
                       view=view[r['vid']],
                       color_type=r['tip'],
                       defect=brak,
                       refuse=refuse,
                       features=u'',
                       name=r['prim']
            )

        b.total = int(r['total'])
        b.save()

    db.close()



#total_update()
check()