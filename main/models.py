# -*- coding: utf-8 -*-
from django.db import models
from whs.bricks.models import bricks
#from dojango.forms import DateField,DateInput

#class BrickWidget(model.ForeignKey)


class oper(models.Model):
    brick=models.ForeignKey(bricks,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Кол-во кирпича для операции')
    time_change=models.DateTimeField(auto_now=True)
    # DRAFT ДЛЯ ПРОСТОТЫ!!!! ПОДУМАТЬ!!!

    class Meta:
        abstract = True


class doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))

    number=models.PositiveIntegerField(unique=True,verbose_name=u'№ документа',help_text=u'Число')
    doc_date=models.DateField(u'Дата',max_length=60,help_text=u'Дата документа')
    info=models.CharField(u'Примечание',max_length=60,blank=True,help_text=u'Любая полезная информация')
    time_change=models.DateTimeField(auto_now=True)
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True
