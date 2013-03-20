import datetime
import pandas as pd
from pandas import *
import numpy as np
import scipy
import statsmodels

import csv

from bkz.lab.models import *
from bkz.make.models import *


from django.core.management.base import BaseCommand, CommandError


randn = np.random.randn

class Command(BaseCommand):
    help = "Commands for static analize"

    def handle(self, *args, **options):
        label = args[0]
        if label:
            getattr(self, label)()


    def export(self):
    	writer = csv.writer(open('../pandas.csv','wb'))
        writer.writerow(['forming_date','density','amount','warren_date','tts','tto','batch_date','defect'])
    	for p in Part.objects.filter(warrens__isnull=False):
            for w in p.warrens.all():
                for q in w.consumer.filter(forming__isnull=False):
                    writer.writerow([q.forming.date,q.forming.density,q.forming.width.tts,q.date,q.tts,w.tto,p.batch.date,p.batch.number,p.defect])


    def show(self):
    	data = read_csv('../pandas.csv')
        print data.describe()
