# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from bkz.whs.views import BillCreateView
from django.views.generic import UpdateView

from bkz.lab.models import *
from bkz.lab.forms import *
from bkz.whs.forms import DateForm,YearMonthFilter

class BatchCreateView(BillCreateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]
    def form_valid(self, form):
        self.object = form.save(commit=False)
        width = self.object.width
        if width == 0.8:
            width = 1.0
        self.object.seonr = SEONR.objects.filter(color=self.object.color).latest('date')
        self.object.efflorescence = Efflorescence.objects.filter().latest('date')
        self.object.heatconduction = HeatConduction.objects.filter(width=width).latest('date')
        self.object.frost_resistance = FrostResistance.objects.filter(color=self.object.color).latest('date')
        self.object.water_absorption = WaterAbsorption.objects.filter().latest('date')
        self.object.save()
        return redirect(self.get_success_url())

class BatchUpdateView(UpdateView):
    form_class=BatchForm
    model=Batch
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        self.object = form.save(commit=False)
        for part in self.parts:
            if part.is_valid() and part.has_changed():
                part.save()
            if part.rows.is_valid() and part.instance.pk:
                part.rows.save()
        if self.parts.is_valid():
            self.parts.save()
        self.object.amount = sum([r.instance.out or 0 for r in self.parts])
        self.object.tto = ','.join([r.instance.tto or '' for r in self.parts])
        self.object.save()
        if all([p.is_valid() and p.rows.is_valid() for p in self.parts]):
            messages.add_message(self.request, messages.SUCCESS, u'Партия сохранена успешно!')
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        self.parts = PartFactory(self.request.POST or None, instance=self.object)
        for part in self.parts:
            part.rows = RowFactory(self.request.POST or None, instance=part.instance,prefix=part.prefix+'-row')
        context['parts'] = self.parts
        return context

def index(request):
    queryset = Batch.objects.all().select_related('frost_resistance','width')\
                    .prefetch_related('parts','parts__rows','parts__cause')
    datefilter = YearMonthFilter(request.GET or None,model=Batch)
    if datefilter.is_valid():
        data = dict([(k,v) for k,v in datefilter.cleaned_data.items() if v])
    else:
        date = datetime.date.today()
        data = {'date__year':date.year,'date__month':date.month}
    queryset = queryset.filter(**data)
    return render(request,'lab/index.html',dict(object_list=queryset,datefilter=datefilter))


from webodt.shortcuts import render_to_response
def batch_print_akt(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/akt-out.odt',{'batch':batch},format='pdf',inline=True)


def batch_print_doc(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/document-the-quality-of.odt',{'batch':batch},format='pdf',inline=True)



def batch_tests(request,pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    def preparation(w):
        return [{'type':w,'row':x} for x in sum(map(lambda x: [pow(2,x)]*2,[x for x in xrange(1,5) if x!=2]),[])]
    flexion = FlexionFactory(request.POST or None, instance=batch,initial=preparation('flexion'),
                            queryset=batch.tests.filter(type='flexion'),prefix='flexion')
    pressure = PressureFactory(request.POST or None, instance=batch,initial=preparation('pressure'),
                            queryset=batch.tests.filter(type='pressure'),prefix='pressure')
    form = BatchTestsForm(request.POST or None,instance=batch)
    if request.method == 'POST':
        if form.is_valid():
            batch = form.save()
            messages.add_message(request, messages.SUCCESS, u'Характеристики сохранены!')
        if flexion.is_valid():
            flexion.save()
            fle = flexion.get_value
            messages.add_message(request, messages.SUCCESS, u'Испытания на изгиб сохранены!')
        if pressure.is_valid():
            pressure.save()
            pre = pressure.get_value
            messages.add_message(request, messages.SUCCESS, u'Испытания на сжатие сохранены!')
        if pressure.is_valid() and flexion.is_valid():
            volume = request.POST.get('volume','')
            if volume:
                factory, i = volume.split('-')
                if factory in ['pressure','flexion']:
                    batch.volume = eval(factory)[int(i)].instance
                    batch.save()
            if pre and fle:
                batch.mark = min((fle['mark'],pre['mark']))
                batch.pressure = pre['avgn']
                batch.flexion = fle['avgn']
                batch.save()
                messages.add_message(request, messages.SUCCESS, u'Марка определена!')
                return redirect(batch.get_tests_url())
            else:
                messages.add_message(request, messages.WARNING, u'Не хватает данных для определения марки!')
    return render(request,'lab/batch-tests.html',{'tests':[pressure,flexion],'batch':batch,'form':form})

def batch_tests_print(request,pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    flexion = batch.tests.filter(type='flexion')
    pressure = batch.tests.filter(type='pressure')
    return render(request,'lab/batch-tests-print.html',{'tests':[pressure,flexion],'batch':batch})


def journal(request,date=None):
    f = DateForm(request.GET or None)
    if f.is_valid():
        date = f.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    date = datetime.datetime.combine(date,datetime.time(8))
    filter = dict(datetime__range=(date,date+datetime.timedelta(hours=24)))
    clay = ClayFactory(request.POST or None,queryset=Clay.objects.filter(**filter),prefix='clay')
    storedclay = StoredClayFactory(request.POST or None,queryset=StoredClay.objects.filter(**filter),prefix='storedclay')
    sand = SandFactory(request.POST or None,queryset=Sand.objects.filter(**filter),prefix='sand')
    bar = BarFactory(request.POST or None, queryset=Bar.objects.filter(**filter),prefix='bar')
    raw = RawFactory(request.POST or None, queryset=Raw.objects.filter(**filter),prefix='raw')
    raw_initial = [ {'position':16,'path':5},{'position':16,'path':7},
                    {'position':25,'path':5},{'position':25,'path':7}]
    half = HalfFactory(request.POST or None, queryset=Half.objects.filter(**filter),prefix='half',initial=raw_initial)
    factory = [clay, storedclay, sand, bar, raw, half]
    if request.method == 'POST':
        for f in factory:
            if f.is_valid():
                f.save()
    return render(request,'lab/journal.html',{'factory':factory,'date':date,'dateform':f})

def stats(request):
    datefilter = YearMonthFilter(request.GET or None,model=Batch)
    modelselect = ModelSelect(request.GET or None)
    if modelselect.is_valid():
        factory = eval(modelselect.cleaned_data['model']+'Factory')
    else: 
        factory = ClayFactory
    if datefilter.is_valid():
        data = dict([(k.replace('date','datetime'),v) for k,v in datefilter.cleaned_data.items() if v])
    else:
        date = datetime.date.today()
        data = {'datetime__year':date.year,'datetime__month':date.month}
    factory = factory(queryset=factory.model.objects.filter(**data))
    return render(request,'lab/stats.html',{'datefilter':datefilter,'modelselect':modelselect,
        'factory':factory})