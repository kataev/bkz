# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from bkz.lab.models import *

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        label,args = args[0],args[1:]
        if label == 'amount':
            self.amount()
        elif label =='limestone':
            self.limestone()
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
