# -*- coding: utf-8 -*-
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
import dojango.forms as forms
from whs.brick.models import Brick
from django.utils.encoding import force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label')
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}

class CheckBoxBrickSelect(forms.CheckboxSelectMultiple):
    dojo_type = 'whs.form.CheckBox'

class BrickFilterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(BrickFilterForm,self).__init__(*args,**kwargs)
        for k,w in self.fields.iteritems():
            q = w.choices
            choice = []
            for item in q:
                if not item[0] == '': choice.append([Brick.css_dict[k][item[0]],item[1][:7]])
            w.choices = choice

    class Meta:
        model=Brick
        fields = ('mark','brick_class','view','weight','color_type')
        widgets = {
         'mark': CheckBoxBrickSelect(),
         'brick_class': CheckBoxBrickSelect(),
         'view': CheckBoxBrickSelect(),
         'weight': CheckBoxBrickSelect(),
         'color_type': CheckBoxBrickSelect(),
         }
    class Media:
        js = ('js/bricks.js',)
        css = {'all':('css/bricks.css',),}

class BrickSelect(forms.Select):
    dojo_type = 'whs.form.BrickSelect'

    def render(self, name, value, attrs=None, choices=()):
        """ Переопределние метода для вывода нужного тега. """
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name,value=value)
        output = [u'<input%s/>' % flatatt(final_attrs)]
#        output = [u'<input/>']
        return mark_safe(u'\n'.join(output))


class BrickSelectStack(BrickSelect):
    dojo_type = 'whs.form.BrickSelect.StackConteiner'

    def render(self, name, value, attrs=None, choices=()):
        """ Переопределние метода для вывода нужного тега. """
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, brick, selected_choices, option_value=None, option_label=None):
        """
        Переопределние метода для вывода элемента тега с нужными тегами.
        """
        if brick is None:
            return u''
        else:
            selected_html = ((brick.pk in selected_choices) or (
            str(brick.pk) in selected_choices)) and u' selected="selected"' or ''
            return u'<option class="%(class)s" total="%(total)s" value="%(pk)s"%(selected_html)s>%(title)s</option>' % {
                'class': brick.css,
                'total': brick.total,
                'pk': brick.pk,
                'selected_html': selected_html,
                'title': brick
            }

    def render_options(self, choices, selected_choices):
        selected_choices = set([v for v in selected_choices])
        output = []
        br = self.choices.queryset
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    try:
                        val = int(option_value)
                        output.append(self.render_option(br.get(pk=val), selected_choices, *option))
                    except ValueError:
                        output.append(self.render_option(None, selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                try:
                    val = br.get(pk=option_value)
                except:
                    val = None
                output.append(self.render_option(val, selected_choices))
        return u'\n'.join(output)