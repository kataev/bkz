# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from bkz.make.models import Warren,Forming
from itertools import chain,groupby,tee,izip_longest
from string import rjust
import datetime

class Command(BaseCommand):
    help = "Commands for make app"
    def handle(self, *args, **options):
        self.args = args
        label = args[0]
        if label:
            getattr(self,label)()

    def tts_diff(self):
        date = self.args[1]
    	formings = iter(Forming.objects.order_by('date','order').filter(date=date))
    	warrens = iter(Warren.objects.order_by('date','order').filter(date=date))
    	if len(self.args) == 3:
            for i in range(int(self.args[2])):
                formings.next()
    	for f,w in izip_longest(formings,warrens,fillvalue=Forming()):
    		print (f.tts == w.tts),f.tts,w.tts,'\t',f.pk,w.pk
    
    def warren_source(self):
        Warren.objects.all().update(source=None)
        source = None
        for w in Warren.objects.all().order_by('date','order'):
            if w.cause.count():
                w.source = None
            else:
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
        # transaction.commit()
        transaction.rollback()


    @transaction.commit_manually
    def forming_warren(self):
        Warren.objects.all().update(forming=None,part=None)
        delay = datetime.timedelta(1)
        for f in Forming.objects.filter(date__year=2012,date__month=1).order_by('-date','order'):
            warrens = Warren.objects.filter(Q(date=f.date) | Q(date=f.date - delay)).filter(tts=f.tts).order_by('-date')
            if warrens:
                w = warrens[0]
                if not w.forming:
                    w.forming = f
                    w.save()
            else:
                print 'dne',f
        for w in Warren.objects.filter(date__year=2012,date__month=1).order_by('-date','order'):
            if not w.forming:
                formings = Forming.objects.filter(date__lt=w.date - delay).filter(tts=w.tts).order_by('-date')
                print w.order, w, [ f.date for f in formings[:2] ]
        transaction.rollback()


    def forming_vacuum(self):
        vacuum = 0
        for f in Forming.objects.filter(date__year=2012,date__month=1).order_by('date','order'):
            if not f.vacuum == vacuum:
                vacuum = f.vacuum
            elif not f.order == 1:
                f.vacuum = None
            f.save()


    def show(self):
        if len(self.args[1]) > 3:
            args = dict(date = self.args[1])
        else:
            args = dict(tts = self.args[1])
        print 'forming'
        for f in Forming.objects.filter(**args).order_by('-date','order'):
            print f.pk,'\t', rjust(str(f.order),2), f.date, rjust(str(f.tts),4),f.get_color_display(),f.width
        print 'warren'
        for f in Warren.objects.filter(**args).order_by('-date','order'):
            print f.pk,'\t', rjust(str(f.order),2), f.date, rjust(str(f.tts),4), f.get_tto


    def set(self):
        if len(self.args) > 3:
            if self.args[1] == 'warren':
                model = Warren
            elif self.args[1] == 'forming':
                model = Forming
            model.objects.filter(pk=self.args[2]).update(tts=self.args[3])

    
    def test_order(self):
        args = {'date__year':2012,'date__month':1}
        form = ' '.join( str(f.tts) for f in Forming.objects.filter(**args))
        for d in Forming.objects.filter(**args).dates('date','day'):
            warrens = ' '.join( str(f.tts) for f in Warren.objects.filter(date=d))
            formings = ' '.join( str(f.tts) for f in Forming.objects.filter(date=d))
            print d, (warrens in formings),len(formings),len(warrens)


    def fetch_path(self):
        args = {'date__year':2012,'date__month':1}
        for l,s in zip(Warren.objects.filter(**args),Warren.objects.using('server').filter(**args)):
            if l.pk == s.pk:
                l.path = s.path
                l.save()
            else:
                print 'fail'
    

    def forming_order(self):
        args = {'date__year':2012,'date__month':1}
        tts = ''
        path = ''
        for f in Forming.objects.filter(**args):
            tts+='{} '.format(f.tts)
            try:
                p = str(f.warren.path)
            except Warren.DoesNotExist:
                p = ''
            path += rjust(p,4)
        print tts
        print path