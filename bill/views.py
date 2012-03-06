# -*- coding: utf-8 -*-
import datetime

from exceptions import ValueError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max
from django.http import QueryDict
from django.shortcuts import get_object_or_404, render
from error_pages.http import Http403

from whs.bill.forms import BillFilter,Bill
from whs.views import CreateView, UpdateView
from whs.bill.pdf import pdf_render_to_response

__author__ = 'bteam'

class CreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        if not self.request.user.has_perm('%s.add_%s' % (self.model._meta.app_label,self.model._meta.module_name)):
            raise Http403

        if self.request.method == 'GET':
            initial = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (initial.get('number') or 0) + 1
            print context['form'].instance
            context['form'].initial = initial
        print context['form'].initial
        return context

#@permission_required('bill.view_bill')
def bill_print(request,id):
    doc = get_object_or_404(Bill.objects.select_related(),pk=id)
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