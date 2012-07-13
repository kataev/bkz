# -*- coding: utf-8 -*-
__author__ = 'bteam'
class bkzRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'old':
            return 'old'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'old':
            return 'old'
        return None

    def allow_syncdb(self, db, model):
        if db == 'old':
            return False
        elif model._meta.app_label == 'old':
            return False
        return None