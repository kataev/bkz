# -*- coding: utf-8 -*-
__author__ = 'bteam'
from old.models import Tovar, Jurnal, Sclad, Agent as OAgent
from sale.models import *
from manufacture.models import *

def nomenclature():
    """
    Импорт номенклатуры из бух-кой базы
    """
    f = file('bricks.txt', 'r').readlines()
    for l in f:
        n = Nomenclature()
        n.code = l[:12]
        n.title = l[12:-1].strip()
        n.save()

def brick():
    """
    Импорт продукции из старой базы
    """
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
    """
    Ипортирование контрагентов из старой базы и споставление их с бух-кой базой
    """
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
    """
    Импорт "приходов" из старой базы
    """
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
    """
    Синхронизация остатков баз
    """
    for b in OldBrick.objects.all():
        try:
            b.total = Sclad.objects.get(pk=b.old).total
            b.save()
        except Sclad.DoesNotExist:
            print b.pk


def sold():
    """
    Импорт накладных из старой базы данных
    """
    b = Bill()
    for j in Jurnal.objects.filter(minus__gt=0):
        try:
            brick = OldBrick.objects.get(old=j.tov.pk)
            agent = OldAgent.objects.get(old=j.agent.pk)
        except OldAgent.DoesNotExist:
            print j.agent.pk,'\tAgent DNE'
        except OldBrick.DoesNotExist:
            print j.tov.pk,'\tBrick DNE'
        if j.date !=j.date:
            b = Bill(date=j.date,number=j.nakl)
            if j.agent == u'Северная керамика': # Сделать поиск по примичанию для опредления покупателя
                b.agent
                b.seller = u'Северная керамика'
            else:
                b.agent = agent
                b.seller = u'ЗОВОД'
            b.save()

        s = Sold()
        s.brick = brick
        s.amount = j.minus
        s.tara = j.poddon
        s.price = j.price
        s.delivery = j.trans
        s.info = j.prim
        s.doc = b
        s.full_clean()
#        s.save()

def transfer():
    for j in Jurnal.objects.filter(akt_gt=0,pakt_gt=0):
        try:
            brick_to = OldBrick.objects.get(old=j.tov.pk)
            agent = OldAgent.objects.get(old=j.agent.pk)
        except OldBrick.DoesNotExist:
            print j.tov.pk,'\tBrick to DNE'
        except OldAgent.DoesNotExist:
            print j.agent.pk,'\tAgent to DNE'
        s = Sold.objects.filter(brick=brick_to,doc__date=j.date,amount_gte=j.pakt,doc__agent=agent)
        if len(s):
            s = s.get()
            b = s.doc
            t = Transfer(doc=b,amount=j.pakt)
            try:
                t.brick_from = OldBrick.objects.get(old=Jurnal.objects.get(akt=j.akt,makt_gt=0).tov.pk)
            except OldBrick.DoesNotExist:
                print j.tov.pk,'\tBrick DNE'
            t.brick_to = brick_to
            t.tara = s.poddon
            t.price = s.price
            t.delivery = s.trans
            t.info = j.prim

            if s.amount > j.pakt:
                s.mount-=j.pakt
                s.save()
            else:
                t.info+=s.info
                s.delete
            t.full_clean()
            t.save()
        else:
            print j.pk,'\tSold DNE'

ft = dict(fullname = 'name', name = 'name',address = 'address',phone = 'phone',inn = 'inn',bank = 'bank',ks = 'schet')
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
#                b.save()
                for n in [f.name for f in Agent._meta.fields][1:]:
                    if getattr(a,n) == 'None' or not getattr(a,n):
                        if ft.get(n,False):
                            setattr(a,n,getattr(o,ft[n]))
#                a.save()
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
#                a.save()
                break
            except Agent.MultipleObjectsReturned:
                if len(name) == i+1:
                    try:
                        OldAgent.objects.get(old=o.pk)
                        break
                    except OldAgent.DoesNotExist:
                        pass
                    print '%s ' * len(name) % tuple(name), o.pk, o.name
                    for i,e in enumerate(q[:3]):
                        print '\t',i+1,e.name,e.pk,e.buhagent.code
                    r = raw_input()
                    if r == 'e':
                        continue
                    a = q[int(r)-1]
                    b = OldAgent(agent_ptr=a)
                    b.old = o.pk
                    b.save()
                    for n in [f.name for f in Agent._meta.fields][1:]:
                        if getattr(a,n) == 'None' or not getattr(a,n):
                            if ft.get(n,False):
                                setattr(a,n,getattr(o,ft[n]))
                    a.save()
                    break
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
#    man()
#    totals()
#    old_agents()
    agent_test()