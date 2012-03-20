# -*- coding: utf-8 -*-
__author__ = 'bteam'
from old.models import *
from brick.models import *
from buh.models import BuxAgent

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
        a = BuxAgent()
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

if __name__ == '__main__':
#    brick()
    agents()