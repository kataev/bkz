# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import CreateView

from bkz.it.models import *
from django.db.models import Count,Sum

def main(request):
    """ Главная страница """
    d = Device.objects.all()
    w = Work.objects.all().select_related()[:10]
    c = Buy.objects.all().select_related()[:10]
    replaces = Plug.objects.order_by('-date').all().select_related()[:10]

    buy = dict(Buy.objects.values_list('cartridge_id').order_by().annotate(Sum('amount')))
    plug = dict(Plug.objects.values_list('bill__cartridge').order_by().annotate(Count('id')))

    totals = dict([(pk,v-plug.get(pk,0)) for pk,v in buy.items()])

    return render(request, 'it/it.html',dict(divices=d,works=w,cons=c,totals=totals,replaces=replaces))


class PlugCreateView(CreateView):
    def get_initial(self):
        initial = self.initial.copy()
        if self.request.method == 'GET':
            agent = self.request.GET.get('bill', None)
            if agent:
                initial['bill'] = agent
        return initial

class BuyCreateView(CreateView):
    def get_initial(self):
        initial = self.initial.copy()
        if self.request.method == 'GET':
            agent = self.request.GET.get('cartridge', None)
            if agent:
                initial['cartridge'] = agent
        return initial