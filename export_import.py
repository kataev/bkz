# -*- coding: utf-8 -*-
from whs.models import BuhAgent, Nomenclature, Seller, OldAgent, Agent, Sold, Bill, Add, Man, Sorted, Sorting, Brick

__author__ = 'bteam'
from old.models import *
from man.models import *

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
    for t in DispTovar.objects.all().filter(pk=295):
        try:
            OldBrick.objects.get(old=t.id)
        except OldBrick.DoesNotExist:
            print 'not found, processing...'
        b = OldBrick()
        b.old = t.id
        b.name = t.name
        b.mark = t.mark
        b.prim = t.prim
        if t.vid == u'Строительный':
            b.view = u'Р'
        else:
            b.view = u'Л'

        if t.mas == u'Полуторный':
            b.width = 1.4
        if t.mas == u'Одинарный':
            b.width = 1.0
        if t.color == u'КЕ':
            b.width == 0.8
        if t.color == u'Двойной':
            b.width == 0.0

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
        print 'new pk %d' % b.pk


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
    for j in DispJurnal.objects.filter(plus__gt=0).order_by('date'):
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
    for b in DispTovar.objects.select_related().all():
        try:
            o = OldBrick.objects.get(old=b.pk)
            o.total = b.total.total
            o.save()
        except OldBrick.DoesNotExist:
            print b.pk,b.prim

def get_agent(name):
    name = name.replace(u'ИП', '').replace(u'ООО', '').replace(u'"', '').replace(u'-', ' ')\
    .replace(u'\\', ' ').replace(',', ' ').strip().split(' ')
    name = filter(None, name)
    q = Agent.objects.all()
    for i, n in enumerate(name):
        q = q.filter(name__icontains=n)
        try:
            a = q.get()
        except Agent.DoesNotExist:
#            print 'DNE','%s ' * len(name) % tuple(name)
            return None
        except Agent.MultipleObjectsReturned:
            if i == len(name) -1:
#                print 'MOR','%s ' * len(name) % tuple(name)
                return None

def sold():
    """
    Импорт накладных из старой базы данных
    """
    zavod = Seller.objects.get(pk=1206)
    sk = Seller.objects.get(pk=1175)
    b = Bill()
    for j in DispJurnal.objects.filter(minus__gt=0).order_by('nakl','-date',):
        try:
            brick = OldBrick.objects.get(old=j.tov.pk)
        except OldBrick.DoesNotExist:
            print j.tov.pk,'\tBrick DNE'
        n = int(j.nakl.split('/')[0])
        if b.number != n:
            b = Bill(date=j.date,number=n)
            print n,j.date
            if j.agent.pk == 1:
                if '/' in j.prim:
                    ag,prim = j.prim.split('/')
                    agent = get_agent(ag)
                    b.info = prim
                elif '"' in j.prim:
                    ag,prim = j.prim.split('"')[1:]
                    agent = get_agent(ag)
                    b.info = prim
                else:
                    agent = get_agent(j.prim) or sk
                    b.info = j.prim
#                print agent,b.info,j.prim
                b.agent = agent or sk
                b.seller = sk
            else:
                try:
                    b.agent = OldAgent.objects.get(old=j.agent.pk)
                except OldAgent.DoesNotExist:
                    a = OldAgent()
                    o = j.agent
                    a.fullname = o.name
                    a.name = o.name
                    a.address = o.address
                    a.phone = o.phone
                    a.inn = o.inn
                    a.bank = o.bank
                    a.ks = o.schet
                    a.old = o.pk
                    a.full_clean()
                    a.save()
                    b.agent = a
                b.seller = zavod
            b.full_clean()
            b.save()

        s = Sold()
        s.doc = b
        s.brick = brick
        s.amount = j.minus
        s.tara = j.poddon
        s.price = j.price
        s.delivery = j.trans
        s.info = j.prim
        s.full_clean()
        s.save()

def transfer():
    dne = 0
    dl = 0
    for j in DispJurnal.objects.filter(akt__gt=0,pakt__gt=0):
        print j.pk
        try:
            brick_to = OldBrick.objects.get(old=j.tov.pk)
        except OldBrick.DoesNotExist:
            print j.tov.pk,'\tBrick to DNE'
        s = Sold.objects.filter(brick=brick_to,doc__date=j.date)
        if len(s):
            try:
                s = s.get()
            except Sold.MultipleObjectsReturned:
                s = s[0]
            b = s.doc
            t = Sold(doc=b,amount=j.pakt)
            try:
                t.brick_from = OldBrick.objects.get(old=DispJurnal.objects.get(akt=j.akt,makt__gt=0).tov.pk)
            except OldBrick.DoesNotExist:
                print j.tov.pk,'\tBrick DNE'
            t.brick = brick_to
            t.tara = j.poddon
            t.price = j.price
            t.delivery = j.trans
            t.info = j.prim

            if s.amount > j.pakt:
                s.amount-=j.pakt
                t.tara = s.tara
                t.price = s.price
                t.delivery = s.delivery
                s.full_clean()
                s.save()
            elif s.amount == j.pakt:
                t.info+=s.info
                s.full_clean()
                t.tara = s.tara
                t.price = s.price
                t.delivery = s.delivery
                dl+=1
                s.delete()
            else:
                pass
            t.full_clean()
            t.save()
        else:
            print j.pk,'\tSold DNE'
            dne += 1
    print 'dne',dne
    print 'del',dl

ag  = [22L, 40L, 45L, 79L, 114L, 123L, 134L, 155L, 221L, 234L, 277L, 353L]
ag1 = [74L, 86L, 117L, 136L, 161L, 234L, 297L, 328L, 331L, 356L, 393L, 388L]
ft = dict(fullname = 'name', name = 'name',address = 'address',phone = 'phone',inn = 'inn',bank = 'bank',ks = 'schet')
def old_agents():
    dne = 0
    mor = 0
    ok = 0
    for o in DispAgent.objects.all().filter(pk__in=ag1):
        name = o.name.replace(u'ИП', '').replace(u'ООО', '').replace(u'"', '').replace(u'-', ' ')\
        .replace(u'\\', ' ').replace(',', ' ').strip().split(' ')
        name = filter(None, name)
        q = Agent.objects.all()
        for i, n in enumerate(name):
            q = q.filter(name__icontains=n)
            try:
                a = q.get()
                ok+=1
                try:
                    a.oldagent
                    if a.oldagent.old == o.pk:
                        print '=='
                    else:
                        print '!='
                        f = DispAgent.objects.get(pk=o.pk)
                        t = DispAgent.objects.get(pk=a.oldagent.old)
                        print DispJurnal.objects.filter(agent=f).update(agent=t),'updated'
                        if not DispJurnal.objects.filter(agent=f).count():
                            o.delete()
                    break
                except OldAgent.DoesNotExist:
                    pass

                b = OldAgent(agent_ptr=a)
                b.old = o.pk
#                b.save()
                for n in [f.name for f in Agent._meta.fields][1:]:
                    if getattr(a,n) == 'None' or not getattr(a,n):
                        if ft.get(n,False):
                            setattr(a,n,getattr(o,ft[n]))
#                a.save()
                print a.pk,b.pk,'ok',o.name
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
                    dne+=1
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
#                    a.save()
                    break
                continue

    print 'OK ', ok
    print 'DNE', dne
    print 'MOR', mor
    print 'TOT', dne + mor

def agent_test():
    w = []
    for o in DispAgent.objects.all():
        try:
            OldAgent.objects.get(old=o.pk)
        except OldAgent.DoesNotExist:
            print o.name,o.pk
            w.append(o.pk)
    print w,len(w)

def agent_clear():
    for a in Agent.objects.all():
        for n in [f.name for f in Agent._meta.fields][1:]:
            if getattr(a,n) == 'None':
                setattr(a,n,'')
                a.save()

def sorting():
    s = Sorting()
    for j in DispJurnal.objects.filter(mws__gt=0).order_by('-date'):
        if s.date != j.date:
            s = Sorting()
            s.date = j.date
            s.brick = OldBrick.objects.get(old=j.tov.pk)
            s.amount = j.mws
            s.full_clean()
            s.save()


def srted():
    s = Sorted()
    for j in DispJurnal.objects.filter(workshop__gt=0).order_by('-date'):
        if s.date != j.date:
            s = Sorting()
            s.date = j.date
            s.brick = OldBrick.objects.get(old=j.tov.pk)
            s.amount = j.mws
            s.full_clean()
            s.save()


def excell():
    import csv
    from collections import Counter
    oborot = tuple(csv.reader(open('/home/bteam/Dropbox/Оборотная ведомость БКЗ 2012.csv','rb')))
    c = Counter([int(r[0]) for r in oborot if r[0]])
    print [k for k,v in c.iteritems() if v>1]
    for r in filter(lambda r:r[0],oborot):
        pk,total =  r[0],int(r[10])
        b = Brick.objects.get(pk=pk)
        if b.total != total:
            print b.pk,'\t------------------------------------'
            print 'base\t%d\t%s' % (b.total,b.name)
            print 'csv\t%d\t%s' % (total,r[1])
            print 'total:',b.total - total
    print 'base\t',sum([b.total for b in Brick.objects.all()])
    print 'csv\t',sum([int(r[10]) for r in oborot if r[0]])


if __name__ == '__main__':
#    brick()
#    agents('../agents.txt')
#    man()
    totals()
#    excell()
#    old_agents()
#    agent_test()
#    agent_clear()
#    sold()
#    transfer()
#    sorting()