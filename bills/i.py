# -*- coding: utf-8 -*-
import MySQLdb
import pytils
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


def jurnal():
    db= MySQLdb.connect('localhost','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from jurnal order by id;")
    data = FetchOneAssoc(cursor)

    for r in data:
        if r['minus']>0:
            i=1000
            try:
                n= int(str(r['nakl']).split('/')[0])
            except :
                n = i
                i+=1

            s = sold.objects.get(brick=bricks.objects.get(pk=r['tov']),
                                 amount=int(r['minus']),tara=int(r['poddon']),
                                 price=float(r['price']),
                                 info=pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=r['date']))
            b = bill.objects.get(number=n)
#            print s
            try:
                b = bill.objects.get(number=n)
            except :
                try:
                    b = bill(number=n,doc_date=r['date'],info=r['prim'],agent=agent.objects.get(pk=int(r['agent'])))
                    b.save()
                    b.solds.create(brick=bricks.objects.get(pk=r['tov']),amount=int(r['minus']),tara=int(r['poddon']),price=float(r['price']))
#                    print s
                    s.save()
#                    b.solds.add(s)
#                    b.save()
                except :
                    pass




        if r['akt']>0 :
#            print 'akt'
            if int(r['pakt'])>0:
                try:
                    t = transfer(brick=bricks.objects.get(pk=r['tov']),amount=int(r['pakt']),tara=int(r['poddon']))
                    akt = db.cursor()
                    akt.execute('select tov from jurnal where akt=%d and makt > 0;' % int(r['akt']))

                    tov = akt.fetchone()[0]
                    t.info = u'Это перевод перенесенный из старой базы, он полностью не поддежривается. Перенос был в %s, id:%d %s' % (bricks.objects.get(pk=tov),tov,pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=r['date']))
    #                    t = transfer(brick=bricks.objects.get(pk=r['tov']),amount=int(r['pakt']),tara=int(r['poddon']))
                    t.save()
                except :
                    print 'error'



    db.close()



jurnal()