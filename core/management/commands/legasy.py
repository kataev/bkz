# -*- coding: utf-8 -*-
from docutils.nodes import option
from django.core.management.base import LabelCommand
from whs.models import *
from old.models import *

class Command(LabelCommand):
    help = "Commands for lagasy db"
    def handle_label(self, label, **options):
        if label == 'totals':
            self.totals()
        if label == 'set_old_brick':
            self.set_old_brick(options[0],option[1])

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

