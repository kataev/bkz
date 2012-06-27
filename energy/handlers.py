# -*- coding: utf-8 -*-
__author__ = 'bteam'
from piston.handler import BaseHandler
from piston.utils import rc
import qsstats
import datetime

from django.db.models import Sum

from whs.man.models import Add
from whs.energy.models import Energy,Teplo
from whs.energy.views import delta

class EnergyHandler(BaseHandler):
    allowed_methods = ('GET','PUT')
    model = Energy
    fields = ('date','elec4','elec16','iwater','uwater','gaz')

    def read(self, request, *args, **kwargs):
        """
        Вывод дельты энергоресурсов в виде json
        """
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name
        if pkfield in kwargs:
            try:
                return self.queryset(request).get(pk=kwargs.get(pkfield))
            except self.model.ObjectDoesNotExist:
                return rc.NOT_FOUND
            except self.model.MultipleObjectsReturned: # should never happen, since we're using a PK
                return rc.BAD_REQUEST
        else:
            queryset = self.queryset(request).filter(*args, **kwargs)
            queryset = delta(queryset,self.fields)
            return queryset