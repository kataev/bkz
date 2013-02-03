# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from bkz.lab.models import *
from bkz.whs.models import Width
from bkz.make.models import Warren,Forming
from random import randint,random,shuffle,uniform
from itertools import cycle,chain
import datetime

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        label = args[0]
        if label == 'amount':
            self.amount()
        elif label =='limestone':
            self.limestone()
        elif label == 'forming':
            self.forming()
        else:
            raise CommandError('Command DNE')

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
            a =  p.info.split(u'изв')[0].split(u'ТТО')[1].split(u'прис')[0].split(u'изв')[0].split(u'ивз')[0]
            a = a.replace(u'№','').strip()
            p.limestone = a
            p.save()

    def forming(self):
        i=0
        for h in chain(Half.objects.all(),Raw.objects.all(),Bar.objects.all()):
            try:
                h.forming = Forming.objects.filter(date__lt=h.datetime.date()).filter(tts=h.tts).order_by('-date')[0]
                h.save()
            except IndexError:
                print i,'DNE',h