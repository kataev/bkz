# -*- coding: utf-8 -*-
__author__ = 'bteam'
from whs.bill.models import *
from random import randrange
import datetime

def fill_bills(count):
    agents = Agent.objects.all()
    bricks = Brick.objects.all()
    for i in range(count):
        d = datetime.date.today() - datetime.timedelta(randrange(2))
        b = Bill(agent=agents[randrange(len(agents)-1)],date=d,number=i)
        b.save()

        for o in range(randrange(1,3)):
            s = Sold(amount=randrange(288,28800),brick=bricks[randrange(len(bricks)-1)],price=randrange(10),doc=b)
            s.save()