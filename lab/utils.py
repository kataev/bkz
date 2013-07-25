# -*- coding: utf-8 -*-
import datetime
import re

tto_regexp = re.compile(r'(?:(\d+)-?(\d*))+')


def convert_tto(tto):
    """ Split '12-25,11' to array """
    return sum([range(int(b), int(e or b) + 1) for b, e in tto_regexp.findall(tto)], [])


def get_min_avg_max(tests):
    tests = [t.value for t in tests]
    if tests:
        return min(tests), sum(tests) / len(tests), max(tests)
    else:
        return 0, 0, 0


def get_shift(date=datetime.datetime.now(), shift=True):
    """Определние смены по времени, {0:дневная,1:ночная}"""
    start1 = date.replace(hour=8, minute=0, second=0, microsecond=0)
    end1 = date.replace(hour=20, minute=0, second=0, microsecond=0)
    if shift:
        hours = 12
    else:
        hours = 24
    if date < start1:
        return 1, (start1 - datetime.timedelta(hours=hours), start1)
    elif start1 < date < end1:
        return 0, (start1, start1 + datetime.timedelta(hours=hours))
    else:
        return 1, (end1, end1 + datetime.timedelta(hours=hours))


class ShiftMixin(object):
    def get_shift_display(self):
        date = self.datetime
        shift, range = get_shift(date)
        if not shift:
            return u'Дневная смена'
        else:
            return u'Ночная смена'
