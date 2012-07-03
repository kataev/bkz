# -*- coding: utf-8 -*-
import datetime
import logging

from exceptions import ValueError
from django.db.models import Max,Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext as _

from whs.sale.forms import BillFilter, Bill, Agent,YearMonthFilter, BillAggregateFilter
from whs.views import CreateView, UpdateView, DeleteView, ListView
from whs.sale.pdf import pdf_render_to_response

logger = logging.getLogger(__name__)

__author__ = 'bteam'

class BillSlugMixin(object):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        year = self.kwargs.get('year', None)
        number = self.kwargs.get('number', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif year is not None and number is not None:
            queryset = queryset.filter(date__year=year, number=number)

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object pk or a slug."
            % self.__class__.__name__)

        try:
            obj = queryset.get()
        except self.model.DoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class UpdateView(BillSlugMixin, UpdateView):
    pass


class DeleteView(BillSlugMixin, DeleteView):
    pass


class CreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            initial = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (initial.get('number') or 0) + 1
            print context['form'].instance
            context['form'].initial = initial
        print context['form'].initial
        return context

def bill_pk_redirect(request,pk):
    b = get_object_or_404(Bill,pk=pk)
    return redirect(b.get_absolute_url())


def bill_print(request, year, number):
    doc = get_object_or_404(Bill.objects.select_related(), number=number, date__year=year)
    return pdf_render_to_response('torg-12.rml', {'doc': doc})

class BillListView(ListView):
    queryset = Bill.objects.prefetch_related('solds','pallets','solds__brick','solds__brick_from').select_related()
    template_name = 'bills.html'
    paginate_by = 20
    context_object_name = 'bills'

    def get_paginate_by(self, queryset):
        try:
            p = int(self.request.GET.get('rpp',''))
        except ValueError:
            p = self.paginate_by
        return p

#    def get_queryset(self):
#        form = BillFilter(self.request.GET or None)
#        if form.is_valid():
#            data = dict([(k,v) for k,v in form.cleaned_data.items() if v is not None])
#            if data.has_key('page'):
#                data.pop('page')
#            if data.has_key('year'):
#                data['date__year']=data.pop('year')
#            if data.has_key('month'):
#                data['date__month']=data.pop('month')
#            if data.has_key('brick'):
#                data['solds__brick']=data.pop('brick')
#            if data.has_key('rpp'):
#                data.pop('rpp')
#            return self.queryset.filter(**data)
#        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        context['form'] = BillFilter(self.request.GET or None)
        return context

def agents(request):
    alphabet = u"АБВГДЕЁЖЗИКЛМНОПРСТФХЦЧШЩЫЮЯ"
    Agents = Agent.objects.all()
    letter = request.GET.get('b','')
    if letter:
        Agents = Agents.filter(name__iregex=u"^%s." % letter[0])
    return render(request, 'agents.html', dict(Agents=Agents,alphabet=alphabet))


def stats(request):
    form = YearMonthFilter(request.GET or None)
    return render(request, 'stats.html',dict(form=form))
