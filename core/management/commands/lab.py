# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from bkz.lab.models import *
from bkz.whs.models import Width
from bkz.make.models import Warren,Forming
from random import randint,random,shuffle,uniform
from itertools import cycle
import datetime

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        label = args[0]
        if label == 'amount':
            self.amount()
        elif label =='limestone':
            self.limestone()
        elif label == 'half':
            self.create_test_data_half()
        elif label == 'raw':
            self.create_test_data_raw()
        elif label == 'bar':
            self.create_test_data_bar()
        elif label == 'sand':
            self.create_test_data_sand()
        elif label =='clay':
            self.create_test_data_clay()
        elif label =='storedclay':
            self.create_test_data_stored_clay()
        elif label =='warren':
            self.create_test_data_warren()
            
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

    def create_test_data_stored_clay(self):
        for x in xrange(17):
            print x
            date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
            for i in xrange(randint(2,3)):
                d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
                StoredClay.objects.create(humidity=round(uniform(10,40),2),position=randint(1,5),datetime=d)

        # for x in xrange(17):
        #     date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
        #     for i in xrange(randint(4,6)):
        #         d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
        #         StoredClay.objects.create(datetime=d,position=randint(1,5),humidity=round(random(),2),used=(i==4))


    def create_test_data_clay(self):
        for x in xrange(17):
            date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
            for i in xrange(randint(2,3)):
                d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
                Clay.objects.create(datetime=d,humidity=randint(2,40)+round(random(),2),
                                               sand=randint(2,40)+round(random(),2),
                                               inclusion=randint(2,40)+round(random(),2),
                                               dust=randint(2,40)+round(random(),2),)

    def create_test_data_sand(self):
        for x in xrange(2):
            print x
            date = datetime.date(2013,1,2) + datetime.timedelta(days=randint(1,3))
            for i in xrange(randint(0,3)):
                d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
                Sand.objects.create(datetime=d,humidity=randint(2,40)+round(random(),2),
                                               particle_size=randint(2,40)+round(random(),2),
                                               module_size=randint(2,40)+round(random(),2),)

    tts = [81, 63, 40, 94, 90, 95, 14, 35, 9, 13, 10, 42, 31, 93, 36, 17, 26, 23, 52, 4, 74, 27, 51, 64, 41, 56, 44, 49, 34, 84, 78, 96, 8, 24, 39, 43, 45, 76, 98, 32, 75, 12, 37, 19, 28, 53, 1, 29, 72, 21, 48, 60, 67, 30, 22, 79, 70, 46, 58, 61, 16, 3, 65, 97, 47, 68, 55, 80, 88, 85, 7, 25, 11, 73, 6, 20, 62, 50, 5, 54, 59, 82, 66, 91, 38, 86, 71, 89, 69, 77, 87, 83, 57, 92, 15, 18, 33, 2]
    tto = range(1,30)
    def create_test_data_bar(self):
        i,j = 0,0
        width = 1
        color = 0
        tts = self.tts
        for x in xrange(17):
            print x
            if not len(tts):
                tts = self.tts
            cavitation = 0
            if randint(0,40)==0: cavitation = 1
            i+=1
            if i==8:
                width = randint(1,3)
                i=0
            j+=1
            if j==12:
                color = randint(0,2)
                j=0
            date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
            d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
            Bar.objects.create(datetime=d,
                humidity=round(uniform(20,25),2),
                humidity_transporter=round(uniform(12,20),2),
                temperature=round(uniform(30,45),2),
                sand=round(uniform(2,10),2),
                weight = randint(2000,4000),
                color = color_c[color][0],
                width = Width.objects.get(pk=width))
    def create_test_data_bar_tts(self):
        for b,t in zip(Bar.objects.all().order_by('datetime'),cycle(self.tts)):
            b.tts = t
            b.save()

    def create_test_data_raw(self):
        shuffle(self.tts)
        i,j = 0,0
        width = 1
        color = 0
        tts = self.tts
        for x,t in zip(xrange(17),cycle(self.tts)):
            if not len(tts):
                tts = self.tts
            i+=1
            if i==8:
                width = randint(1,3)
                i=0
            j+=1
            if j==12:
                color = randint(0,2)
                j=0
            date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
            d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
            Raw.objects.create(
                datetime=d,
                color = Bar.objects.filter(datetime__year=2013,datetime__month=d.month,datetime__day=d.day)[0].color,
                width = Bar.objects.filter(datetime__year=2013,datetime__month=d.month,datetime__day=d.day)[0].width,

                tts = t,
                temperature=round(uniform(30,40),2),
                size = '%d.0 x %d.0 x %d.0' % (272-randint(0,2),129-randint(0,2),95-randint(0,2)),
                # sand=randint(2,10)+round(random(),2),
                weight = randint(2000,4000),
                humidity=round(uniform(2,40),2),
                )

    def create_half(self,d,color,width,pos,path,t):
        if pos==16:
            weight = randint(4100,4208)
            hum = round(uniform(12,13),2)
        else:
            weight = randint(3700,3800)
            hum = round(uniform(2,8),2)
        return Half.objects.create(
            datetime=d,
            color = color,
            width = width,
            position = pos,
            path = path,
            tts = t,
            size = '%d.0 x %d.0 x %d.0' % (255-randint(0,2),121-randint(0,2),88-randint(0,2)),
            weight = weight,
            humidity=hum,
            shrink=round(uniform(5,7),2)
            )

    def create_test_data_half(self):
        shuffle(self.tts)
        i,j = 0,0
        width = 1
        color = 0
        tts = self.tts
        for x in xrange(17):
            print x
            for q,t,path,pos in zip(range(3),cycle(self.tts),cycle([5,7]),cycle([16,16,25,25])):
                if not len(tts):
                    tts = self.tts
                i+=1
                if i==8:
                    width = randint(1,3)
                    i=0
                j+=1
                if j==12:
                    color = randint(0,2)
                    j=0
                date = datetime.date(2013,1,1) + datetime.timedelta(days=x)
                d = datetime.datetime.combine(date,datetime.time(randint(8,12),randint(0,59)))
                self.create_half(d, color, Width.objects.get(pk=width), pos, path, t)

                

    def create_test_data_warren(self):
        ttss = cycle(self.tts)
        for batch in Batch.objects.all():
            d = batch.date - datetime.timedelta(days=5)
            for tto in batch.get_tto:
                warren = Warren.objects.create(date=d,number=tto,amount='')
                for i,tts in zip(range(5),ttss):
                    Warren.objects.create(date=d,number=tts,source=warren,amount='')


    def get_tto_period(self):
        dr = (datetime.date(2013,1,1),datetime.date(2013,1,31))
        result = []
        for i in xrange(1,30):
            a = map(lambda x: (datetime.date(2013,1,1)-x).days,[t.part.batch.date for t in RowPart.objects.filter(part__batch__date__range=dr) if i in t.get_tto])
            w = None
            r = []
            for j,q in enumerate(a):
                if w is not None:
                    r.append(w-q)
                w=q
            result.append(r)
            print r




