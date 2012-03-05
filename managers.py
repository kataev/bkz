# -*- coding: utf-8 -*-
from django.db import models
import datetime

class CurrendMonthDateManager(models.Manager):
    def get_query_set(self):
        date = datetime.date.today().replace(day=1)
        return super(CurrendMonthDateManager, self).get_query_set().filter(doc__date__gte=date)


class CurrendMonthDateDocManager(models.Manager):
    def get_query_set(self):
        date = datetime.date.today().replace(day=1)
        return super(CurrendMonthDateDocManager, self).get_query_set().filter(date__gte=date)