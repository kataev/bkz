# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from models import Brick,BrickTable
from bill.models import *
from piston.utils import rc
import django.forms as forms
import datetime
from django.db.models import Q,Sum,F

class BrickHandler(BaseHandler):
    allowed_methods = ('GET')
    model = Brick
    fields = ('id', 'label','css','total')

def date_inital():
    return datetime.date.today().replace(day=1)

class DateForm(forms.Form):
    date = forms.DateField(initial=date_inital,required=False)

class BrickTableHandler(BaseHandler):
    allowed_methods = ('GET')
    model = BrickTable
    fields = ('id', 'label','css','total','begin','add','t_from','t_to','sold')

    def read(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED
        if 'id' in kwargs:
            try:
                f = DateForm(request.GET)
                if f.is_valid():
                    date = f.cleaned_data.get('date') or date_inital()
                    brick = self.model.objects.get(pk=kwargs.get('id'))
                    tablebrick = BrickTable(pk=brick.pk,label=brick.label,css=brick.css,total=brick.total)
                    tablebrick.sold = Sold.objects.filter(doc__date__gte=date,brick=brick).aggregate(s=Sum('amount'))['s']
#                    brick.add = Add.objects.filter(doc__date__gte=date,brick=brick).aggregate(s=Sum('amount'))['s']
                    tablebrick.t_from = Transfer.objects.filter(doc__date__gte=date,brick=brick).aggregate(s=Sum('amount'))['s']
                    tablebrick.t_to = Sold.objects.filter(doc__date__gte=date,transfer__doc__date__gte=date,brick=brick).aggregate(s=Sum('amount'))['s']
                    return tablebrick
                else:
                    return rc.BAD_REQUEST
            except self.model.DoesNotExist:
                return rc.NOT_FOUND
            except self.model.MultipleObjectsReturned: # should never happen, since we're using a PK
                return rc.BAD_REQUEST
        else:
            f = DateForm(request.GET)
            if f.is_valid():
                date = f.cleaned_data.get('date') or date_inital()

                sold = Sold.objects.filter(doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
                t_from = Transfer.objects.filter(doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
                t_to = Sold.objects.filter(doc__date__gte=date,transfer__doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
                sold = dict(map(lambda x: [x['brick'],x['s']],sold))
                t_from = dict(map(lambda x: [x['brick'],x['s']],t_from))
                t_to = dict(map(lambda x: [x['sold__brick'],x['s']],t_to))
                queryset = []
                for b in Brick.objects.all():
                    brick = BrickTable(pk=b.pk,label=b.label,css=b.css,total=b.total)
                    brick.total = b.total
                    brick.sold = sold.get(b.pk,0)
                    brick.add = 0
                    brick.t_from = t_from.get(b.pk,0)
                    brick.t_to = t_to.get(b.pk,0)
                    brick.begin = brick.total + brick.sold + brick.t_from - brick.t_to
                    queryset.append(brick)
            return queryset