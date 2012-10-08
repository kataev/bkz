# -*- coding: utf-8 -*-
__author__ = 'bteam'

limit = {
    'flexion': {
        1.0: {
            'avg': [3.4, 2.9, 2.5, 2.3, 2.1, 1.9, 1.6],
            'min': [1.7, 1.5, 1.3, 1.1, 1.0, 0.9, 0.8]
        },
        1.4: {
            'avg': [2.9, 2.5, 2.3, 2.1, 1.8, 1.6, 1.4],
            'min': [1.5, 1.3, 1.0, 1.0, 0.9, 0.8, 0.7]
        },
        },
    'pressure': {
        'avg': [30, 25, 20, 17.5, 15, 12.5, 10],
        'min': [25, 20, 17.5, 15, 12.5, 10, 7.5]
    },
    }


class BatchMixin(object):
    def get_mark_display(self):
        pass

