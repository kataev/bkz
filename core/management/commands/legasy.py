# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from bkz.whs.models import *
from bkz.lab.models import *
from bkz.old.models import *

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        label,args = args[0],args[1:]
        if label == 'totals':
            self.totals()
        if label == 'set_old_brick':
            self.set_old_brick(*args[:2])
        if label == 'test_batch':
            self.test_batch(*args[:3])

    def totals(self):
        for b in DispTovar.objects.select_related().all():
            try:
                o = OldBrick.objects.get(old=b.pk)
                o.total = b.total.total
                o.save()
            except OldBrick.DoesNotExist:
                print 'DNE',b.pk,b.prim

    def set_old_brick(self,pk,old):
        b = Brick.objects.get(pk=pk)
        OldBrick.objects.create(pk=pk,old=old)
        b.save()
        print b,'ok'

    def test_batch(self,year,month,day=None):
        pluss = DispJurnal.objects.filter(plus__gt=0).filter(date__year=year,date__month=month)
        if day: pluss = pluss.filter(date__day=day)
        for plus in pluss.order_by('-date'):
            old = OldBrick.objects.get(old=plus.tov_id)
            part = Part.objects.filter(batch__date=plus.date,defect=old.defect)
            try:
                part = part.get()
                if old.mark != part.batch.mark and old.mark < 400:
                    print 'mark not match', plus.date, old, part.batch.mark
                    continue
                if part.amount == plus.plus:
                    part.brick = old
                    part.save()
                else:
                    print 'amount not match', plus.date, old,plus.plus, '!=' ,part.amount, part.batch.mark
            except Part.DoesNotExist:
                print 'DNE',plus.date,old,plus.plus
            except Part.MultipleObjectsReturned:
                print 'MOR',plus.date,old
