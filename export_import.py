# -*- coding: utf-8 -*-
__author__ = 'bteam'
from old.models import Tovar,Jurnal,Sclad,Agent as OAgent
from sale.models import *
from manufacture.models import *

from copy import deepcopy

def nomenclature():
    f = file('bricks.txt','r').readlines()
    for l in f:
        n = Nomenclature()
        n.code = l[:12]
        n.title = l[12:-1].strip()
        n.save()


def brick():
    for t in Tovar.objects.all():
        b = OldBrick()
        b.old = t.id

        b.name = t.name

        b.mark = t.mark

        if t.vid == u'Строительный':
            b.view = u'Р'
        else:
            b.view = u'Л'

        if t.mas == u'Полуторный':
            b.weight = 1.4
        if t.mas == u'Одинарный':
            b.weight = 1.0
        if t.color == u'КЕ':
            b.weight == 0.8
        if t.color == u'Двойной':
            b.weight == 0.0

        if u'жел' in t.prim:
            b.color = 1
        elif u'кор' in t.prim:
            b.color = 2
        elif u'светлый' in t.prim:
            b.color = 3
        elif u'белый' in t.prim:
            b.color = 4
        else:
            b.color = 0

        if u'-20 ' in t.prim:
            b.defect = u'<20'
        if u'+20' in t.prim:
            b.defect = u'>20'
            b.mark = 9000

        b.label = make_label(b)


        try:
            b.css = make_css(b)
        except IndexError:
            print b.old,b.label

        b.full_clean()
        b.save()

def agents():
    f = file('agents.txt','r').readlines()
    for l in f:
        a = BuhAgent()
        a.pk=1
        fields = l.split('\t')
        a.code = fields[0]
        a.fullname = fields[1]
        a.address = fields[2]
        a.type = fields[3]
        a.name = fields[4]
        a.inn = fields[6]
        a.kpp = fields[7]
        a.bank = fields[9]
        a.rs = fields[10]
        a.ks = fields[11]
        a.bic = fields[12]
        a.full_clean()
        a.save()
        break

def man():
    m = Man()
    for j in Jurnal.objects.filter(plus__gt=0).order_by('date'):
        try:
            brick = OldBrick.objects.get(old=j.tov.pk)
        except :
            continue
        if j.date != m.date:
            m = Man(date=j.date)
            m.save()
        a = Add(brick=brick,amount=j.plus,doc=m)
        a.save()

def totals():
    for b in OldBrick.objects.all():
        try:
            b.total = Sclad.objects.get(pk=b.old).total
            b.save()
        except Sclad.DoesNotExist:
            print b.pk

def bill():
    b = Bill()
    for j in Jurnal.objects.filter(minus__gt=0):
        pass

def old_agents():
    dne = 0
    mor = 0
    for o in OAgent.objects.filter():

        if o.name.split(' ')[0] == u'ООО':
            name= o.name.split(' ')[1]
        else:
            name = o.name.split(' ')[0]
        name = name.strip('"')
        q = Agent.objects.filter(name__iregex=name)
        try:
            a = q.get()
#            print 'ok',o.name
        except Agent.DoesNotExist:
            print 'DN',o.name
            dne+=1
            continue
        except Agent.MultipleObjectsReturned:
            mor+=1
            print 'MOR',o.name
            for i,e in enumerate(q):
                print '\t',i+1,e.name
            r = raw_input()
            if r == 'e':
                continue
            a = q[int(r)-1]
        oa = OldAgent(agent_ptr_id=a.pk)
        oa.old = o.pk
        oa.agent = a
        oa.save()
        a.save()

    print dne
    print mor

#        fullname,o.name
#        address,address
#        phone,phone
#        inn,inn
#        bank,bank
#        ks,schet
#        a.bic
#        a.rc
#        a.info

if __name__ == '__main__':
#    brick()
#    agents()
#    man()
#    totals()
    old_agents()