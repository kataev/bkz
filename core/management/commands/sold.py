from django.core.management.base import BaseCommand
from bkz.whs.models import *
from bkz.lab.models import *
from bkz.old.models import *
from random import randint
class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        self.totals()

    def totals(self):
        for i in xrange(200):
            b = Bill.objects.order_by('?')[0]
            b1,b2 =Brick.objects.order_by('?')[:2]
            s = Sold(doc=b,brick=b1,brick_from=b2,amount=randint(2000,30000),price=2)
            s.save()

