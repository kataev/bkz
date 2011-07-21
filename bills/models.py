# -*- coding: utf-8 -*-
from whs.main.models import doc,oper
from whs.bricks.models import bricks
from whs.agents.models import agent
from django.db import models

import dojango.forms as forms
import pytils
from django.utils.encoding import StrAndUnicode, force_unicode
from itertools import chain
from django.contrib.humanize.templatetags.humanize import intcomma
from django.forms.util import flatatt
from django.utils.safestring import mark_safe



class BrickSelect(forms.Select):
#    dojo_type = 'whs.select.Brick'

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'<div class="brickselect">ololo</div>')
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))
    


    def render_option(self,brick,selected_choices, option_value=None, option_label=None):
#        print brick,selected_choices,option_label,option_value
#        option_value = force_unicode(option_value)
        if brick is None:
#            return u'<option>------</option>'
            return u''
        else:
            selected_html = (brick.pk in selected_choices) and u' selected="selected"' or ''
            return u'<option dojoType="whs.br" class="%(class)s" cl="%(cl)s" mark="%(mark)s" view="%(view)s" weight="%(weight)s" total="%(total)s" value="%(pk)s"%(selected_html)s>%(title)s</option>' % {
                'class':brick.show_css(),
                'cl':brick.get_brick_class_display(),
                'mark':brick.get_mark_display(),
                'view':brick.get_view_display(),
                'weight':brick.get_weight_display(),
                'total':intcomma(brick.total),
                'pk':brick.pk,
                'selected_html':selected_html,
                'title':brick

            }

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([v for v in selected_choices])
        output = []
        br =  bricks.objects.all().order_by('pk')
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    try:
                        print option_value
                        val = int(option_value)
                        output.append(self.render_option(br.get(pk=val),selected_choices,*option))
                    except ValueError:
                        output.append(self.render_option(None,selected_choices,*option))
                output.append(u'</optgroup>')
            else:
                try:
                    val = br.get(pk=option_value)
                except :
                    val = None
                output.append(self.render_option(val,selected_choices))
        return u'\n'.join(output)

class bills_filter_form(forms.Form):
    date1 = forms.DateField(required=False,widget=forms.DateInput(attrs={'style':'width:90px;'}),help_text=u'Дата или начало периода')
    date2 = forms.DateField(required=False,widget=forms.DateInput(attrs={'style':'width:90px;'}),help_text=u'Конец периода')
    brick = forms.ModelChoiceField(required=False,queryset=bricks.objects.all(),help_text=u'Кирпич',widget=BrickSelect())
    agent = forms.ModelChoiceField(required=False,queryset=agent.objects.all(),widget=forms.FilteringSelect(attrs={'style':'width:160px;'}),help_text=u'Контрагент')
    number = forms.CharField(required=False,widget=forms.NumberSpinnerInput(attrs={'style':'width:80px;','constraints':{'min':1}}),help_text=u'Номер накладной')





class sold(oper):
    price=models.FloatField(u"Цена за единицу",help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
    delivery=models.FloatField(u"Цена доставки",blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfers,blank=True,null=True,help_text=u'Перевод для этой продажи')

    class Meta():
            verbose_name = u"Отгрузка"
            verbose_name_plural =  u"Отгрузки"

    def __unicode__(self):
        return u'Отгрузка № %d %s, %d шт' % (self.pk,self.brick,self.amount)

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)


class soldForm(forms.ModelForm):
    class Meta:
        model=sold
        exclude=('post')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'brick': BrickSelect()
         }

class transfer(oper):
    sold = models.ForeignKey(sold,blank=True,null=True,verbose_name=u'Отгрузка') #Куда
    class Meta():
            verbose_name = u"Перевод"
            verbose_name_plural = u"Переводы"

    def __unicode__(self):
        if self.sold is None:
            return u'Незаконченный перевод № %d из %s, %d шт' % (self.pk,self.brick,self.amount)
        else:
            return u'Перевод № %d из %s в %s, %d шт' % (self.pk,self.brick,self.sold.brick,self.amount)

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)

class transferForm(forms.ModelForm):
    class Meta:
        model=transfer
        exclude=('post')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'brick': BrickSelect()
         }

## Накладная
class bill(doc):
    agent = models.ForeignKey(agent,verbose_name=u'КонтрАгент')
    solds = models.ManyToManyField(sold,blank=True,null=True,help_text=u'Отгрузки',verbose_name=u'Отгрузки')
    transfers = models.ManyToManyField(transfer,blank=True,null=True,help_text=u'Переводы',verbose_name=u'Переводы')

    class Meta():
            verbose_name = u"Накладная"
            verbose_name_plural = u"Накладные"
            ordering = ['-doc_date']

    def __unicode__(self):
        return u'Накладная № %d от %s %s' % (self.number,pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.doc_date),self.agent.name[:50])

    def get_absolute_url(self):
        return "/form/%s/%i/" % (self._meta.module_name,self.id)

    def posting(self):
        transfers = self.transfers.all()
        solds = self.solds.all()

        errors= []
        for t in transfers: # Обрабатываем
            t.brick.total +=t.amount
            t.sold.brick.total -= t.amount
        for s in solds:
            s.brick.total -=s.amount

        for t in transfers: # Проверяем
            if t.brick.total < 0:
                error = {'brick':t.brick,'amount':t.brick.total*-1,'error':u'Не хватает кирпича','oper':t}
                errors.append(error)
            if t.sold.brick.total < 0:
                error = {'brick':t.sold.brick,'amount':t.sold.brick.total*-1,'error':u'Не хватает кирпича в принимащей строне',"oper":t}
                errors.append(error)
        for s in solds:
            if s.brick.total < 0:
                error = {'brick':s.brick,'amount':s.brick.total*-1,'error':u'Не хватает кирпича','oper':s}
                errors.append(error)
        if len(errors) > 0:
            return errors
        else:
            for t in transfers:
                t.brick.save()
                t.sold.brick.save()
                t.post=True

            for s in solds:
                s.brick.save()
                s.post=True
            self.draft=True
            return []



class billForm(forms.ModelForm):
    class Meta:
        model=bill
        exclude=('draft')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'brick': BrickSelect()
         }
