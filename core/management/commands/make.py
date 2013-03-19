# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from bkz.make.models import Warren,Forming
from itertools import chain,groupby,tee,izip_longest
import datetime

class Command(BaseCommand):
    help = "Commands for make app"
    def handle(self, *args, **options):
        label = args[0]
        if label:
            getattr(self,label)()

    def tts_test(self):
    	date = datetime.date(2012,1,16)
    	formings = iter(Forming.objects.order_by('date','order').filter(date=date))
    	warrens = iter(Warren.objects.order_by('date','order').filter(date=date))
    	print date
    	for f,w in izip_longest(formings,warrens,fillvalue=Forming()):
    		print (f.tts == w.tts),f.tts,w.tts
    
    def warren_source(self):
        Warren.objects.all().update(source=None)
        source = None
        for w in Warren.objects.all().order_by('date','order'):
            if w.tto:
                source = w
            w.source = source
            w.save()

    @transaction.commit_manually
    def warren_forming(self):
        Warren.objects.all().update(forming=None,part=None)
        delay = datetime.timedelta(1)
        for w in Warren.objects.filter(date__year=2012,date__month=1).order_by('-date','order'):
            forming = Forming.objects.filter(date__lt=w.date - delay).filter(tts=w.tts).order_by('-date')
            if forming:
                w.forming = forming[0]
                try:
                    w.full_clean()
                except ValidationError:
                    print w.tts,'\t', w.date, [ f.date for f in forming[:2] ], forming[0].warren.date
                else:
                    w.save()
            else:
                print 'dne',w
        transaction.rollback()

    @transaction.commit_manually
    def forming_warren(self):
        Warren.objects.all().update(forming=None,part=None)
        delay = datetime.timedelta(1)
        for f in Forming.objects.filter(date__year=2012,date__month=1).order_by('date','order'):
            warrens = Warren.objects.filter(Q(date=f.date) | Q(date=f.date - delay)).filter(tts=f.tts).order_by('-date')
            if warrens:
                w = warrens[0]
                if w.forming:
                    print 'ololo'
                else:
                    w.forming = f
                    w.save()
            else:
                print 'dne',f
        for w in Warren.objects.filter(date__year=2012,date__month=1).exclude(cause__code='empty').order_by('-date','order'):
            if not w.forming:
                print w,w.cause.all()
        transaction.rollback()