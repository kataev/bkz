# -*- coding: utf-8 -*-
__author__ = 'bteam'
from old.models import Tovar, Jurnal, Sclad, Agent as OAgent
from sale.models import *
from manufacture.models import *

def nomenclature():
    f = file('bricks.txt', 'r').readlines()
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
            print b.old, b.label

        b.full_clean()
        b.save()


def agents(path):
    f = file(path, 'r').readlines()
    for l in f:
        fields = l.split('\t')
        if fields[14].strip() == 'False':
            a = BuhAgent()
            a.code = fields[0]
            a.fullname = fields[1]
            a.address = fields[2]
            a.form = fields[3]
            a.name = fields[4]
            a.inn = fields[6]
            a.kpp = fields[7]
            a.bank = fields[9]
            a.rs = fields[10]
            a.ks = fields[11]
            a.bic = fields[12]
            a.type = fields[13]

            a.full_clean()
            a.save()
            print a.pk


def man():
    m = Man()
    for j in Jurnal.objects.filter(plus__gt=0).order_by('date'):
        try:
            brick = OldBrick.objects.get(old=j.tov.pk)
        except:
            continue
        if j.date != m.date:
            m = Man(date=j.date)
            m.save()
        a = Add(brick=brick, amount=j.plus, doc=m)
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
    for o in OAgent.objects.all():
        name = o.name.replace(u'ИП', '').replace(u'ООО', '').replace(u'"', '').replace(u'-', ' ')\
        .replace(u'\\', ' ').replace(',', ' ').strip().split(' ')
        name = filter(None, name)
        q = Agent.objects.all()
        for i, n in enumerate(name):
            q = q.filter(name__icontains=n)
            try:
                a = q.get()
                b = OldAgent(agent_ptr=a)
                b.old = o.pk
                b.save()
                a.save()
                print a
                break
            except Agent.DoesNotExist:
                dne += 1
#                print '%s ' * len(name) % tuple(name), o.pk
                a = OldAgent()
                a.fullname = o.name
                a.name = o.name
                a.address = o.address
                a.phone = o.phone
                a.inn = o.inn
                a.bank = o.bank
                a.ks = o.schet
                a.old = o.pk
                a.full_clean()

                print a
#                a.save()
                break
            except Agent.MultipleObjectsReturned:
                if len(name) == i+1:
                    print '%s ' * len(name) % tuple(name), o.pk
                    for i,e in enumerate(q[:3]):
                        print '\t',i+1,e.name,e.pk,e.buhagent.code
                continue

    print 'DNE', dne
    print 'MOR', mor
    print 'TOT', dne + mor

def agent_test():
    w = []

    for o in OAgent.objects.all():
        try:
            OldAgent.objects.get(old=o.pk)
        except OldAgent.DoesNotExist:
            w.append(o.pk)
    print w

if __name__ == '__main__':
#    brick()
#    agents('../agents.txt')
    agents('../agents_post.txt')
#    man()
#    totals()
#    old_agents()
#    agent_test()