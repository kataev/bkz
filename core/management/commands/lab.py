# -*- coding: utf-8 -*-
from itertools import chain, groupby, tee, izip
from operator import attrgetter
import datetime

from django.core.management.base import BaseCommand, CommandError
from bkz.lab.models import *
from bkz.make.models import Warren, Forming


class Command(BaseCommand):
    help = "Commands for lab app"

    def handle(self, *args, **options):
        label = args[0]
        if label:
            getattr(self, label)()

    def amount(self):
        for p in Part.objects.prefetch_related('rows'):
            p.amount = sum([r.out for r in p.rows.all()])
            p.tto = ','.join([r.tto for r in p.rows.all()])
            p.save()
        for b in Batch.objects.select_related('parts'):
            b.amount = sum([p.amount for p in b.parts.all()])
            b.tto = ','.join([p.tto for p in b.parts.all()])
            b.save()
        print 'ok'

    def limestone(self):
        for p in Part.objects.exclude(info=''):
            a = p.info.split(u'изв')[0].split(u'ТТО')[1].split(u'прис')[0].split(u'изв')[0].split(u'ивз')[0]
            a = a.replace(u'№', '').strip()
            p.limestone = a
            p.save()

    def forming(self):
        i = 0
        for h in Half.objects.all():
            try:
                h.forming = Forming.objects.filter(date__lt=h.datetime.date()).filter(tts=h.tts).order_by('-date')[0]
                h.save()
            except IndexError:
                i += 1
                print i, 'DNE', h

        for h in chain(Raw.objects.all(), Bar.objects.all()):
            try:
                h.forming = Forming.objects.filter(date__lte=h.datetime.date()).filter(tts=h.tts).order_by('-date')[0]
                h.save()
            except IndexError:
                i += 1
                print i, 'DNE', h


    def convert_tts(self):
        tts = ((200, 45), (300, 72), (400, 134), (600, 74), (500, 52), (222, 110))
        for m in [Forming, Warren, Raw, Bar, Half]:
            for old, new in tts:
                m.objects.filter(tts=old).update(tts=new)

    def order(self):
        for model in (Half, Raw, Bar, Matherial):
            queryset = model.objects.extra(select={'date': 'DATE(datetime)'}).order_by('date', 'order')
            for g, l in groupby(queryset, key=attrgetter('date')):
                for i, m in enumerate(l):
                    m.order = i + 1
                    m.save()


    def parts(self):
        for w in Warren.objects.filter(tto__isnull=False).order_by('date'):
            d1 = w.date
            d2 = w.date + datetime.timedelta(7)
            for tto in set(w.get_tto):
                try:
                    b = Batch.objects.filter(date__gt=d1).filter(tto__regex=r'^(\[%d,)|(, %d,)|(, %d\])' % ((tto,) * 3)).order_by('date')[0]
                    for p in b.parts.all():
                        if tto in p.get_tto:
                            w.part = p
                            w.save()
                            print 'saved'
                except IndexError:
                    print d1, '<', w.date, '<', d2, w, w.tto, tto

    def enumerated(self):
        line = []
        for b in Batch.objects.filter(date__year=2012, date__month=1).order_by('date'):
            data = sorted(convert_tto(','.join(r.tto or '' for r in b.parts.all())))
            # print b.date,data
            if (max(data) - min(data)) > 10:
                data = sum(sorted((list(g) for v, g in groupby(data, lambda x: x > 20)), reverse=True), [])
                # if min(data) != 1:
            print b.pk, b.date, data, [t.tto for t in b.parts.all()]
            line += data

        def pairwice(iterable):
            a, b = tee(iterable)
            next(b, None)
            return izip(a, b)

        for a, b in pairwice(line):
            if a - b > 1:
                print a, b