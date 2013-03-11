# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
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
