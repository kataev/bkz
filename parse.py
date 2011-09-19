# -*- coding: utf-8 -*-
import MySQLdb

from whs.brick.models import Brick,OldBrick

def FetchOneAssoc(cursor) :
    data = cursor.fetchall()
    if not data:
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
    db= MySQLdb.connect('server','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from sclad,tovar where sclad.id=tovar.id order by sclad.id;")
    data = FetchOneAssoc(cursor)
    b = {}

    for q in data:
        b['b'+str(q['id'])]=q


    for w in bricks.objects.values_list('id').all():
        try:
            del(b['b'+str(w[0])])
        except KeyError,e:
            print w[0],e

    print b

def total_update():
    db= MySQLdb.connect('localhost','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from sclad,tovar where sclad.id=tovar.id order by sclad.id;")
    data = FetchOneAssoc(cursor)
    for r in data:
        try:
            b = OldBrick.objects.get(old_id=int(r['id']))
        except OldBrick.DoesNotExist:
            view={u'Строительный':u'Р',u'Лицевой':u'Л'}
            weight={u'Полуторный':u'1.4',u'Двойной':u'2',u'Одинарный':u'1',u'Прочее':u'2'}
            class_c = {u'Красный':0,u'Желтый':1,u'Коричневый':2,u'Светлый':3,u'Белый':4,u'КЕ':5,u'Прочее':6}
            color = {u'Красный':u'Кр',u'Желтый':u'Же',u'Коричневый':u'Ко',u'Светлый':u'Св','Белый':u'Бе',u'\u0411\u0435\u043b\u044b\u0439':u'Бе',u'Белый':u'Бе',u'КЕ':u'Кр',u'Прочее':u'Кр'}
#            print r
            if not r['mark']:
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
            old_id=r['id']
            try:
                brick_class=class_c[r['color']]
                color=color[r['color']]
            except KeyError,e:
                print 'keyerror',e,r['id']
                brick_class=0
                color=u'Кр'
            mark=mark
            weight=weight[r['mas']]
            view=view[r['vid']]
            color_type=r['tip']
            defect=brak
            refuse=refuse
            features=u''
            name=r['prim']
#            print r
            b = OldBrick(old_id=r['id'],brick_class=brick_class,color=color,mark=mark,weight=weight,view=view,color_type=color_type,defect=defect
                         ,refuse=refuse,features=features,name=name)

            b.save()
#        b.total = int(r['total'])
    db.close()

total_update()

