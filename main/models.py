# -*- coding: utf-8 -*-
from django.db import models
from whs.bricks.models import bricks
#import dojango.forms as forms

class oper(models.Model):

    poddon_c = ((288,u'Маленький поддон'),(352,u'Обычный поддон'))

#    post_c=((False,u'Не проведенно'),(True,u'Проведенно'))
    brick=models.ForeignKey(bricks,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
    amount=models.PositiveIntegerField(u"Кол-во кирпича",help_text=u'Кол-во кирпича для операции')
    tara=models.PositiveIntegerField(u"Кол-во поддонов",default=0)
    poddon=models.PositiveIntegerField(u"Тип поддона",choices=poddon_c,default=1)
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
    post=models.BooleanField(u'Проведенно?',default=False)
    # DRAFT ДЛЯ ПРОСТОТЫ!!!! ПОДУМАТЬ!!!
    attr={}
    class Meta:
        abstract = True

    def widget(self,selected_html='',as_tr=False,attrs={}):
        attrs={
            'selected_html':selected_html,
            'value':self.pk,
            'name':self._meta.module_name,
            'amount':self.amount,
            'tara':self.tara,
            'info':unicode(self.info),
            'brick_css':self.brick.show_css(),
            'brick':unicode(self.brick),
            'brick_value':self.brick.pk
        }
        attrs.update(self.attr)
        at = u''
        for a in attrs:
            
            at += u'%s="%s" ' %(unicode(a),unicode(attrs[a]))
        if as_tr:
            template = u'<option dojoType="whs.oper_tr" %s >%s</option>' % (at,unicode(self))
        else:
            template = u'<div dojoType="whs.oper" %s>%s</div>' % (at,unicode(self))
        return template

class doc(models.Model):
    draft_c=((False,u'Чистовик'),(True,u'Черновик'))
    
    number=models.PositiveIntegerField(unique=True,verbose_name=u'№ документа',help_text=u'Число')
    doc_date=models.DateField(u'Дата',help_text=u'Дата документа')
    info=models.CharField(u'Примечание',max_length=300,blank=True,help_text=u'Любая полезная информация')
#    time_change=models.DateTimeField(auto_now=True)
    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')

    class Meta:
        abstract = True
#        ordering = ['-doc_date']
