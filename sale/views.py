# -*- coding: utf-8 -*-
import datetime
import logging
import re

from exceptions import ValueError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max
from django.http import QueryDict, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from whs.sale.forms import BillFilter, Bill, Agent
from whs.views import CreateView, UpdateView, DeleteView
from whs.sale.pdf import pdf_render_to_response
from whs.sale.models import Transfer,Sold,Bill

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


def bill_print(request, year, number):
    doc = get_object_or_404(Bill.objects.select_related(), number=number, date__year=year)
    return pdf_render_to_response('torg-12.rml', {'doc': doc})


def main(request):
    Bills = Bill.objects.select_related().all()
    form = BillFilter(request.GET or None)
    order = request.GET.get('order')
    if order in map(lambda x: x.name, Bill._meta.fields):
        Bills = Bills.order_by(order)

    if form.is_valid() and request.GET:
        d = form.cleaned_data
        d = dict([[x, d[x]] for x in d if d[x]])
        if 'brick' in d.keys():
            d['sale_sold_related__brick'] = d['brick']
            del d['brick']
        Bills = Bills.filter(**d)
    paginator = Paginator(Bills, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bills = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bills = paginator.page(paginator.num_pages)

    opers = {}
    if len(bills.object_list):
        for m in (Transfer,Sold):
            name = m._meta.object_name
            for o in m.objects.select_related().filter(doc__in=bills.object_list):
                d = opers.get(o.doc_id,{})
                a = d.get(name,[])
                a.append(o)
                d[name] = a
                opers[o.doc_id] = d

        for b in bills.object_list:
            b.opers = opers.get(b.pk,{})

#    money = sum([b.money for b in bills.object_list])
#    total = sum([b.total for b in bills.object_list])

#    url = QueryDict('', mutable=True)
#    get = request.GET.copy()
#    get = dict([[x, get[x]] for x in get if get[x]])
#    if get.has_key('page'): del get['page']
#    url.update(get)



    return render(request, 'bills.html', dict(Bills=bills, Filter=form,))# total=total, money=money, url=url.urlencode()))

alphabet = [u"А",u"Б",u"В",u"Г",u"Д",u"Е",u"Ё",u"Ж",u"З",u"И",u"К",u"Л",u"М",u"Н",u"О",u"П",u"Р",u"С",u"Т",u"Ф",u"Х",u"Ц",u"Ч",u"Ш",u"Щ",u"Ы",u"Ю",u"Я"]

def agents(request):
    Agents = Agent.objects.all()
    letter = request.GET.get('b','')
    if letter:
        Agents = Agents.filter(name__iregex=u"^%s." % letter[0])
    return render(request, 'agents.html', dict(Agents=Agents,alphabet=alphabet))