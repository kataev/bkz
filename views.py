# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import transaction
from django.http import QueryDict
from django.db.models import Sum

from whs.brick.models import History
from whs.manufacture.forms import *
from whs.bill.forms import *
from django.contrib import messages
from whs.brick import signals


@require_http_methods(["GET",])
def main(request):
    """ Главная страница """ #
    fields = dict([ (x,Sum(x)) for x in ['begin', 'add', 't_from', 't_to', 'sold', 'total'] ])
    totals = Brick.objects.aggregate(**fields)

    messages.debug(request, '%s SQL statements were executed.' % 2)
    messages.info(request, 'Three credits remain in your account.')
    messages.success(request, 'Profile details updated.')
    messages.warning(request, 'Your account expires in three days.')
    messages.error(request, 'Document deleted.')

    return render(request, 'index.html',dict(totals=totals))

def bills(request):
    Bills = Bill.objects.all()
    form = BillFilter(request.GET or None)
    order = request.GET.get('order')
    if order in map(lambda x: x.name,Bill._meta.fields):
        Bills = Bills.order_by(order)

    if form.is_valid():
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
    money = reduce(lambda memo,b: memo+b.money,bills.object_list,0)
    total = reduce(lambda memo,b: memo+b.total,bills.object_list,0)

    url = QueryDict('',mutable=True)
    get = request.GET.copy()
    get = dict([ [x,get[x]] for x in get if get[x]])
    if get.has_key('page'): del get['page']
    url.update(get)
    return render(request,'bills.html',dict(Bills=bills,Filter=form,total=total,money=money,url=url.urlencode()))

def agents(request):
    Agents = Agent.objects.all()
    paginator = Paginator(Agents, 20) # Show 25 contacts per page

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        agents = paginator.page(page)
    except (EmptyPage, InvalidPage):
        agents = paginator.page(paginator.num_pages)
    return render(request,'agents.html',dict(Agents=agents))



def journal(request):
    form = DateForm(request.GET or None)
    if form.is_valid(): date = form.cleaned_data.get('date')
    else: date = datetime.date.today()

    Jounal = list(Bill.objects.select_related().filter(date=date))+list(Man.objects.select_related().filter(date=date))

    return render(request,'journal.html',dict(Journal=Jounal,date=form))


def bill(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Bill.objects.select_related(),pk=id)
    else: doc = None
    if request.method == 'POST':
        form = BillForm(request.POST,instance=doc,prefix='bill')
        sold = SoldFactory(request.POST,instance=doc,prefix='sold')
        transfer = TransferFactory(request.POST,instance=doc,prefix='transfer')
        if form.is_valid() and sold.is_valid() and transfer.is_valid():
            doc = form.save()
            with transaction.commit_on_success():
                sold.save()
                transfer.save()
            return redirect(doc)
    else:
        initial = {}
        if not id:
            initial = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (initial.get('number') or 0) + 1
        form = BillForm(instance=doc,prefix='bill',initial=initial)
        sold = SoldFactory(instance=doc,prefix='sold')
        transfer = TransferFactory(instance=doc,prefix='transfer')

    return render(request, 'doc.html',dict(doc=form,opers=[sold,transfer]))

def flat_form(request,Form,id):
    """ Форма  """
#    id = args[0]
    if id: model = get_object_or_404(Form._meta.model,pk=id)
    else: model = None
    if request.method == 'POST':
        form = Form(request.POST,instance=model)
        if form.is_valid():
            model = form.save()
            return redirect(model)
    else:
        form = Form(instance=model)

    return render(request, 'flat-form.html',dict(form=form))

def man(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Man.objects.select_related(),pk=id)
    else: doc = None

    if request.method == 'POST':
        form = ManForm(request.POST,instance=doc,prefix='man',)
        add = AddFactory(request.POST,instance=doc,prefix='add')
        if form.is_valid() and add.is_valid():
            try:doc = form.save()
            except ValidationError,e: pass
            form.errors['__all__']=['test']
            add.save()
            return redirect(doc)
    else:

        form = ManForm(instance=doc,prefix='man')
        add = AddFactory(instance=doc,prefix='add')

    return render(request, 'doc.html',dict(doc=form,opers=[add]))


def test(request):
    number = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(Max('number')).get('number__max', 1)
    number = (number or 0) + 1

    bill = Bill.objects.create(number=number,agent=Agent.objects.get(pk=1))
    sold = Sold.objects.create(brick=Brick.objects.get(pk=1),amount=100,tara=1,doc=bill,price=1)

    sold.save()
    transfer = Transfer.objects.create(brick=Brick.objects.get(pk=2),amount=100,tara=1,doc=bill)
#    transfer.save()
    sold.transfer.add(transfer)
    return render(request,'index.html')


def history(request):
    if request.POST:
        for b in Brick.objects.order_by('pk').all():
            date=datetime.date.today().replace(day=1)
            h = History(brick=b,date=date)
            for f in ['begin', 'add', 't_from', 't_to', 'sold', 'total']:
                setattr(h,f,getattr(b,f))
            h.save()
            b.begin = b.total
            for f in [ 'add', 't_from', 't_to', 'sold', 'total']:
                setattr(b,f,0)
            b.save()
        return redirect('/')
    date = datetime.date.today().replace(day=1)
    if date.month == 12:
        date = date.replace(year=date.year-1,month=1)
    f = DateForm(request.GET or None,initial={'date':date})
    if f.is_valid():
        date = f.cleaned_data.get('date').replace(day=1)

    history = History.objects.filter(date=date)

    dates = History.objects.dates('date','month')

    return render(request,'history.html',dict(History=history,date=dates))


