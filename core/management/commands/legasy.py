# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from whs.models import *
from lab.models import *
from old.models import *

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
        for plus in pluss.order_by('date'):
            part = Part.objects.filter(batch__date=plus.date,amount=plus.plus)
            old = OldBrick.objects.get(old=plus.tov_id)
            try:
                part = part.get()
            except Part.MultipleObjectsReturned:
                part = part.filter(batch__mark = old.mark).get()
            except Part.DoesNotExist:
                print 'DNE',plus.plus,plus.date,old
            part.brick = old
            part.save()