# -*- coding: utf-8 -*-
import datetime
import colorbrewer
import pandas as pd
from pandas import *
import numpy as np
import scipy
import statsmodels

import csv

from bkz.lab.models import *
from bkz.make.models import *
from bkz.whs.constants import *


from django.core.management.base import BaseCommand, CommandError


from pandas.tools.plotting import *
from matplotlib.pylab import plt

class Command(BaseCommand):
    help = "Commands for static analize"

    def handle(self, *args, **options):
        label = args[0]
        if label:
            getattr(self, label)()


    def export(self):
        with open('../pandas.csv','wb') as file:
            writer = csv.writer(file,delimiter=';',quoting=csv.QUOTE_NONE)
            head = False
            for x,b in enumerate(Batch.objects.filter(date__year=2012,date__month=1)):
                ro = [ getattr(b,f.name,None) for f in b._meta.fields]
                print b
                for i,p in enumerate(b.parts.all()):
                    row = ro + [ getattr(p,f.name,None) for f in p._meta.fields]
                    print '\t', p
                    for j,w in enumerate(p.warrens.all()):
                        print '\t\t', w
                        for l,q in enumerate(w.consumer.filter(forming__isnull=False)):
                            if head == False:
                                head = True
                                header = [ 'batch_'+f.name for f in b._meta.fields]
                                header += [ 'part_'+f.name for f in p._meta.fields]
                                header += [ 'warren_'+f.name for f in w._meta.fields]
                                header += [ 'forming_'+f.name for f in w.forming._meta.fields]
                                
                                writer.writerow(header)
                            new = row + [ getattr(q,f.name,None) for f in q._meta.fields]
                            new += [ getattr(q.forming,f.name,None) for f in q.forming._meta.fields]
                            print '\t\t\t', q
                            r = []
                            for e in new:
                                if isinstance(e,unicode):
                                    e = unicode(e).encode('utf-8')
                                r.append(e)
                            writer.writerow(r)

    def show(self):
        marks = sorted(dict(mark_c).keys())
        defects = {'gost':'o',u'<20':'-',u'>20':'+',u'no_cont':'x'}
        
    	data = read_csv('../pandas.csv', delimiter=';', quoting=csv.QUOTE_NONE)
        d = data.ix[:,['forming_density','batch_flexion','batch_pressure']]
        colors = [ [round(x/255.,4) for x in colorbrewer.Paired[7][marks.index(mark)]] for mark in data.batch_mark]
        # defects = [ (1, 1, 0) for defect in data.part_defect]
        scatter_matrix(d, alpha=1, diagonal='kde', c=colors, edgecolors='none')#, marker=defects)
        plt.show()