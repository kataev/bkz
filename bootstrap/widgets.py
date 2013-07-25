from django.forms.widgets import Input, RadioInput, RadioFieldRenderer, RadioSelect, TextInput, CheckboxSelectMultiple, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from itertools import chain


class CheckboxSelectMultipleInline(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s" class="checkbox inline"' % final_attrs['id']
            else:
                label_for = 'class="checkbox inline"'
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<label%s>%s %s</label>' % (label_for, rendered_cb, option_label))
        return mark_safe(u'\n'.join(output))


class OptionsRadioInput(RadioInput):
    def __unicode__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'<label%s>%s <span>%s</span></label>' %
                         (label_for, self.tag(), choice_label))


class OptionsRadioRenderer(RadioFieldRenderer):
    def render(self):
        return mark_safe(u'<ul class="inputs-list">\n%s\n</ul>' %
                         u'\n'.join([u'<li>%s</li>' %
                                     force_unicode(w) for w in self]))


class OptionsRadio(RadioSelect):
    renderer = OptionsRadioRenderer


class AppendedText(TextInput):
    def render(self, name, value, attrs=None):
        append_text = self.attrs.get('text', '')
        return mark_safe(u'%s<span class="add-on">%s</span>' % (super(AppendedText, self).render(name, value, attrs),
                                                                append_text))


class PrependedText(TextInput):
    def render(self, name, value, attrs=None):
        prepend_text = self.attrs.get('text', '')
        return mark_safe(
            u'<span class="add-on">%s</span>%s' % (prepend_text, super(PrependedText, self).render(name, value, attrs)))


class AppendPrependText(TextInput):
    def render(self, name, value, attrs=None):
        append_text, prepend_text = self.attrs.get('append_text', ''), self.attrs.get('prepend_text', '')
        return mark_safe(u'<span class="add-on">%s</span>%s<span class="add-on">%s</span>' % (
        prepend_text, super(AppendPrependText, self).render(name, value, attrs), append_text))


class EmailInput(Input):
    input_type = 'email'

    def render(self, name, value, attrs=None):
        append_text = self.attrs.get('text', '@')
        return mark_safe(u'%s<span class="add-on">%s</span>' % (super(EmailInput, self).render(name, value, attrs),
                                                                append_text))
