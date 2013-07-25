# -*- coding: utf-8 -*-
from itertools import chain, cycle

from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.whs.views import BillCreateView
from django.views.generic import UpdateView

from bkz.lab.models import *
from bkz.lab.forms import *
from bkz.whs.forms import DateForm, YearMonthFilter
from bkz.lab.utils import convert_tto


class BatchCreateView(BillCreateView):
    form_class = BatchForm
    model = Batch
    opers = [PressureFactory, FlexionFactory, PartFactory]

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
        messages(self.request, u'Партия созданна')
        return redirect(self.get_success_url())


class BatchUpdateView(UpdateView):
    form_class = BatchForm
    model = Batch

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
        self.object.amount = sum(r.instance.out or 0 for r in self.parts)
        self.object.tto = list(set((convert_tto(','.join(r.instance.tto or '' for r in self.parts)))))
        self.object.save()
        if all(p.is_valid() and p.rows.is_valid() for p in self.parts):
            messages.success(self.request, u'Партия сохранена успешно!')
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        self.parts = PartFactory(self.request.POST or None, instance=self.object)
        for part in self.parts:
            part.rows = RowFactory(self.request.POST or None, instance=part.instance, prefix=part.prefix + '-row')
        context['parts'] = self.parts
        return context


def index(request):
    queryset = Batch.objects.all().select_related('frost_resistance', 'width') \
        .prefetch_related('parts', 'parts__rows', 'parts__cause')
    datefilter = YearMonthFilter(request.GET or None, model=Batch)
    date = datefilter.get_date
    data = {'date__year': date.year}
    if datefilter.is_valid() and datefilter.cleaned_data.get('date__month') is not None:
        data['date__month'] = date.month
    queryset = queryset.filter(**data)
    half = {d.date() for d in
            Half.objects.filter(**{k.replace('date', 'datetime'): v for k, v in data.items()}).dates('datetime', 'day')}
    for b in queryset:
        b.journal = b.date in half
    return render(request, 'lab/index.html', dict(object_list=queryset, datefilter=datefilter, date=date))


from webodt.shortcuts import render_to_response


def batch_print_akt(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/akt-out.odt', {'batch': batch}, format='pdf', inline=True)


def batch_print_doc(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    parts = batch.parts.all()
    part, part2 = False, False
    if len(parts) and parts[0].defect == 'gost':
        part = parts[0]
    if len(parts) == 2 and parts[1].defect == 'gost':
        part2 = parts[1]
    return render_to_response('webodt/document-the-quality-of.odt', {'part': part, 'part2': part2}, format='pdf',
                              inline=True)


def batch_tests(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)

    def preparation(w):
        return [{'type': w, 'row': 2 ** x} for x in sorted(range(1, 5) * 2) if x != 2]

    flexion = FlexionFactory(request.POST or None, instance=batch, initial=preparation('flexion'),
                             queryset=batch.tests.filter(type='flexion'), prefix='flexion')
    pressure = PressureFactory(request.POST or None, instance=batch, initial=preparation('pressure'),
                               queryset=batch.tests.filter(type='pressure'), prefix='pressure')
    form = BatchTestsForm(request.POST or None, instance=batch)
    if request.method == 'POST':
        if form.is_valid():
            batch = form.save()
            messages.success(request, u'Характеристики сохранены!')
        if pressure.is_valid() and flexion.is_valid():
            flexion.save()
            fle = flexion.get_value
            pressure.save()
            pre = pressure.get_value
            volume = request.POST.get('volume', '')
            if volume:
                factory, i = volume.split('-')
                if factory in ['pressure', 'flexion']:
                    batch.volume = eval(factory)[int(i)].instance
                    batch.save()
            if pre and fle:
                batch.mark = min((fle['mark'], pre['mark']))
                batch.pressure = pre['avgn']
                batch.flexion = fle['avgn']
                batch.save()
                messages.success(request, u'Марка определена!')
            else:
                messages.warning(request, u'Не хватает данных для определения марки!')
            return redirect(batch.get_tests_url())
    return render(request, 'lab/batch-tests.html', {'tests': [pressure, flexion], 'batch': batch, 'form': form})


def batch_tests_print(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    flexion = batch.tests.filter(type='flexion')
    pressure = batch.tests.filter(type='pressure')
    return render(request, 'lab/batch-tests-print.html', {'tests': [pressure, flexion], 'batch': batch})


def journal(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date', datetime.date.today())
    else:
        date = datetime.date.today()
    date = datetime.datetime.combine(date, datetime.time(8))
    filter = dict(datetime__range=(date, date + datetime.timedelta(hours=23, minutes=59)))

    def prepare_factory(factory, queryset, initial=({},)):
        queryset = queryset.extra(select={'date': 'DATE(datetime)'}).order_by('date', 'order')
        order = max(f.order for f in queryset or (factory.model(),)) + 1
        initial = [dict(init, datetime=date, order=i) for init, i in
                   zip(cycle(initial), range(order, factory.extra + order + 1))]
        name = factory.__name__
        return factory(request.POST or None, queryset=queryset, prefix=name, initial=initial)

    bar = prepare_factory(BarFactory, Bar.objects.filter(**filter))
    raw = prepare_factory(RawFactory, Raw.objects.filter(**filter))
    quarry = prepare_factory(QuarryFactory, Matherial.objects.filter(**filter).filter(position=8),
                             initial=({'position': 8},))
    clay = prepare_factory(ClayFactory, Matherial.objects.filter(**filter).filter(position__lte=7))

    initial = [{'position': position, 'path': path} for path, position in zip([5, 5, 7, 7], [16, 25, 16, 25])]
    half = prepare_factory(HalfFactory, Half.objects.filter(**filter), initial=initial)

    factory = (half, raw, bar, clay, quarry)
    if request.method == 'POST' and all(f.is_valid() for f in factory):
        for f in factory:
            f.save()
        messages.success(request, u'Журнал сохранен')
        return redirect(reverse('lab:journal') + '?date=%s&s=1' % date.date().isoformat())
    if not all(f.is_valid() for f in factory):
        for f in factory:
            print f.prefix, f.errors
    return render(request, 'lab/journal.html', {'factory': factory, 'date': date, 'dateform': dateform, 'add': True})


def slice(request):
    datefilter = YearMonthFilter(request.GET or None, model=Batch)
    date = datefilter.get_date
    data = {'datetime__year': date.year}
    if datefilter.is_valid() and datefilter.cleaned_data.get('date__month') is not None:
        data['datetime__month'] = date.month
    return render(request, 'index.html')


def stats(request):
    datefilter = YearMonthFilter(request.GET or None, model=Batch)
    modelselect = ModelSelect(request.GET or None)
    if modelselect.is_valid():
        factory = eval(modelselect.cleaned_data['model'] + 'Factory')
    else:
        factory = MatherialFactory
    date = datefilter.get_date
    data = {'datetime__year': date.year}
    if datefilter.is_valid() and datefilter.cleaned_data.get('date__month') is not None:
        data['datetime__month'] = date.month
    factory = factory(queryset=factory.model.objects.filter(**data).order_by('datetime'))
    return render(request, 'lab/stats.html', {'datefilter': datefilter, 'modelselect': modelselect,
                                              'factory': factory, 'functions': ('max', 'avg', 'min')})
