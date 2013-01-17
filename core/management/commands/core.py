# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import get_models,get_app
from django.db import connection
import webodt
from django.template import Context

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        self.call()

    def call(self):
        context = {'models':[]}
        for app in map(get_app,['whs','lab','make']):
            for model in get_models(app):
                m = {'name':model.__name__,'fields':[]}
                for f in model._meta.fields:
                    if f.name == 'id':
                        f.verbose_name+=' записи'
                    if f.get_internal_type() == 'ForeignKey':
                        t = 'integer'
                        f.verbose_name= 'ID %s' % f.related.parent_model._meta.verbose_name.lower()
                        f.max_length=11
                    else:
                        t = connection.creation.data_types.get(f.get_internal_type(),'')
                        t = t.split(' ')[0]
                        t = t.split('(')[0]
                    if f.get_internal_type() == 'IntegerField':
                        f.max_length=10
                    m['fields'].append((f.name,t,f.max_length or '',int(f.null),f.verbose_name))
                context['models'].append(m)
        template = webodt.ODFTemplate('models.odt')
        document = template.render(Context(context))
        print document.name
