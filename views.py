# -*- coding: utf-8 -*-
from django.shortcuts import render
from whs.bill.models import Bill
from whs.brick.models import Brick
import re


def main(request):
    return render(request, 'main.html')


def test_brick(request):
    bricks = Brick.objects.all().order_by('id')

    for b in bricks:
        print re
        st = re.U(b.name)

        if re.match(u'\sф',st):
            print (b.pk)


    r = map(lambda x:unicode(x),bricks)
    print len(r)
    res = []
    i = 0
    while i < len(r):
        if r.count(r[i]) > 1:
            res.append({'pk':i+1,'name':r[i],'t':bricks[i].name})
        i=i+1
    return render(request, 'test.html',{'bricks':res})
