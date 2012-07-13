# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

__author__ = 'bteam'

def validate_transfer(brick_from,brick):
    if brick_from.mark < brick.mark:
        raise ValidationError(u'Нельзя делать перевод из меньшей марки в большую')
    if brick_from.weight != brick.weight:
        raise ValidationError(u'Нельзя в переводе менять размер кирпича')