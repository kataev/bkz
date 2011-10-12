# -*- coding: utf-8 -*-
import calendar
import datetime
from exceptions import ValueError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
import django.utils.simplejson
from bill.models import Sold, Transfer
from brick.models import Brick

__author__ = 'bteam'

def brick_store(request,id=None):
    """ Операции за месяц с определённым кирпичем. """
    d = request.GET.get('date')
    if d:
        try:
            d = datetime.datetime.strptime(d,"%Y-%m-%d").date()
        except ValueError,e:
            raise Http404
    else:
        d = datetime.date.today()

    date=(d.replace(day=1),d.replace(day=calendar.monthrange(d.year,d.month)[1]))

    brick = get_object_or_404(Brick,pk=id)
    store = {'label':'label','identifier':'id','items':[]}
    sold = map(lambda x: {'sold':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Sold.objects.filter(brick=brick,doc__date__range=date))
    t_from = map(lambda x: {'t_from':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Transfer.objects.filter(brick=brick,doc__date__range=date))
    t_to = map(lambda x: {'t_to':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Transfer.objects.filter(sold__brick=brick,doc__date__range=date))
    store['items'].extend(sold)
    store['items'].extend(t_to)
    store['items'].extend(t_from)
    store['items'] = sorted(store['items'],key=lambda x: x['date'])
    return HttpResponse(simplejson.dumps(store), mimetype='application/json')