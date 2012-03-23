# -*- coding: utf-8 -*-
import datetime

from exceptions import ValueError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max
from django.http import QueryDict,Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from whs.bill.forms import BillFilter,Bill,DateForm
from whs.views import CreateView, UpdateView, DeleteView
from whs.bill.pdf import pdf_render_to_response

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
            queryset = queryset.filter(date__year=year,number=number)

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

class UpdateView(BillSlugMixin,UpdateView):
    pass

class DeleteView(BillSlugMixin,DeleteView):
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



#@permission_required('bill.view_bill')
def bill_print(request,year,number):
    doc = get_object_or_404(Bill.objects.select_related(),number=number,date__year=year)
    return pdf_render_to_response('torg-12.rml',{'doc':doc})


def bills(request):
    Bills = Bill.objects.select_related().all()
    form = BillFilter(request.GET or None)
    order = request.GET.get('order')
    if order in map(lambda x: x.name,Bill._meta.fields):
        Bills = Bills.order_by(order)

    if form.is_valid() and request.GET:
        d = form.cleaned_data
        d = dict([ [x,d[x]] for x in d if d[x]])
        print d
        if 'brick' in d.keys():
            d['bill_sold_related__brick'] = d['brick']
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
    money = 0# reduce(lambda memo,b: memo+b.money,bills.object_list,0)
    total = 0#reduce(lambda memo,b: memo+b.total,bills.object_list,0)

    url = QueryDict('',mutable=True)
    get = request.GET.copy()
    get = dict([ [x,get[x]] for x in get if get[x]])
    if get.has_key('page'): del get['page']
    url.update(get)
    return render(request,'bills.html',dict(Bills=bills,Filter=form,total=total,money=money,url=url.urlencode()))