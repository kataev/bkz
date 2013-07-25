# -*- coding: utf-8 -*-
import re

from django.db import models
from django.core.validators import RegexValidator
from south.modelsinspector import add_introspection_rules

brocken_regexp = re.compile(ur'(\d?)(?:п|%)?')
validate_brocken_regexp = RegexValidator(brocken_regexp, u'Пример: 50% или 1п или кол-во в шт', 'invalid')


class BrockenCharField(models.CharField):
    default_validators = [validate_brocken_regexp]
    description = u'Slash-separated floats'

    def formfield(self, **kwargs):
        defaults = {'error_messages': {
        'invalid': u'Введите правильное обозначение брака, например: 50% или 1п или кол-во кирпичей'}}
        defaults.update(kwargs)
        return super(BrockenCharField, self).formfield(**defaults)


add_introspection_rules([], ["^bkz\.make\.fields\.BrockenCharField"])
