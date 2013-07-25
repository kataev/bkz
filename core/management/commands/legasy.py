# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core import serializers
from bkz.whs.models import *
from bkz.lab.models import *
from bkz.old.models import *


class Command(BaseCommand):
    help = "Commands for lagasy db"

    def handle(self, *args, **options):
        label, args = args[0], args[1:]
        if label == 'totals':
            self.totals()
        if label == 'set_old_brick':
            self.set_old_brick(*args[:2])
        if label == 'test_batch':
            self.test_batch(*args[:3])
        if label == 'import_batch':
            self.import_batch()

    def totals(self):
        for t in DispTovar.objects.select_related().all():
            try:
                b = OldBrick.objects.get(old=t.pk).brick
                b.total = t.total.total
                b.save()
            except OldBrick.DoesNotExist:
                print 'DNE', t.pk, t.prim

    def set_old_brick(self, pk, old):
        b = Brick.objects.get(pk=pk)
        OldBrick.objects.create(brick=b, old=old, prim=DispTovar.objects.get(pk=old).prim)
        print b, 'ok'

    def test_batch(self, year, month, day=None):
        pluss = DispJurnal.objects.filter(plus__gt=0).filter(date__year=year, date__month=month)
        if day: pluss = pluss.filter(date__day=day)
        for plus in pluss.order_by('-date'):
            old = OldBrick.objects.get(old=plus.tov_id)
            brick = old.brick
            part = Part.objects.filter(batch__date=plus.date, defect=brick.defect)
            try:
                part = part.get()
                if brick.mark != part.batch.mark and brick.mark < 400:
                    print 'mark not match', plus.date, brick, part.batch.mark
                    continue
                if part.amount == plus.plus:
                    part.brick = brick
                    part.save()
                else:
                    print 'amount not match', plus.date, brick, plus.plus, '!=', part.amount, part.batch.mark
            except Part.DoesNotExist:
                print 'DNE', plus.date, brick, plus.plus
            except Part.MultipleObjectsReturned:
                print 'MOR', plus.date, brick

    def import_batch(self):
        try:
            for m in serializers.deserialize('json', file('../bkz_19_01_2013.json').read()):
                name = m.object._meta.module_name.split('.')[-1].lower()
                if name in ['batch', 'part', 'rowpart', 'cause', 'heatconduction', 'seonr', 'frostresistance',
                            'waterabsorption']:
                    if name == 'batch':
                        m.object.volume = None
                    m.save()
        except serializers.base.DeserializationError:
            pass

