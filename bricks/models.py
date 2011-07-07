# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm
#from django.core.exceptions import ValidationError
#from treebeard.mp_tree import MP_Node
#from dojango.data.modelstore import  *


class bricks(models.Model):
    
    euro_view={u'Л':u'УЛ',u'Р':u''} # Для имени
    
    view_c=((u'Л',u'Лицевой'),(u'Р',u'Рядовой'))
    weight_c=((u'1',u'Одинарный'),(u'1.4',u'Утолщенный'),(u'2',u'Двойной'))
    color_c=((u'Кр',u'Красный'),
                   (u'Же',u'Желтый'),
                   (u'Ко',u'Коричневый'),
                   (u'Св',u'Светлый'),
                   (u'Бе',u'Белый'))

    class_c=((0,u'Красный'),
                   (1,u'Желтый'),
                   (2,u'Коричневый'),
                   (3,u'Светлый'),
                   (4,u'Белый'),
                   (5,u'Евро'),
                   (6,u'Прочее'))
    
    mark_c=((100,u'100'),
            (125,u'125'),
            (150,u'150'),
            (175,u'175'),
            (200,u'200'),
            (250,u'250'),
            (9000,u'Брак'))
    
    type_c=(('',''),('1','1 тип'),('2','2 тип'),('3','3 тип'))
    
    
    defect_c=((u'',u''),(u'<20',u'До 20%'),(u'>20',u'Более 20%'))
    refuse_c=((u'',u''),(u'Ф',u'Фаска'),(u'ФП',u'Фаска Полосы'),(u'ФФ',u'Фаска Фаска'),(u'ФФП',u'Фаска Фаска Полосы'))
           
    brick_class=models.IntegerField(u"Класс кирпича",max_length=60, choices=class_c)
    color=models.CharField(u"Цвет",max_length=60, choices=color_c)
    mark=models.PositiveIntegerField(u"Марка",choices=mark_c)
    weight=models.CharField(u"Ширина",max_length=60, choices=weight_c)
    view=models.CharField(u"Вид",max_length=60, choices=view_c)
    color_type=models.CharField(u"Тип цвета",max_length=6,choices=type_c,blank=True)
    defect=models.CharField(u"Брак в %",max_length=60,choices=defect_c,blank=True)
    refuse=models.CharField(u"Особенности",max_length=10,choices=refuse_c,blank=True)
    features=models.CharField(u"Редкие особености",max_length=60,blank=True,help_text=u'Oттенки, тычки и прочее')
    name=models.CharField(u"Имя",max_length=160,default='')
    total=models.PositiveIntegerField(u"Текуший остаток",default=0)
    
    def get_view(self):
        if self.weight==u'2': # Если камень то вида у него нет
            return u''
        
        if self.brick_class!=5: # Если не евро, то вызываю метод из choises
            return self.get_view_display()
        else:
            if self.view not in self.euro_view.keys():
                print (self.pk,self.view)
#            try:
            return self.euro_view[self.view] #Если евро, то подставляем в хитрый словарь
#            except KeyError:
#                return ''
        
    
    def __unicode__(self): # Хитро выебаный код для вывода имени когда вызываем строку
        from string import Template # Шаблоны йоба
        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        
        if self.weight==u'2':
            t = Template(u'КР $mark $defect $refuse $features') # Шаблон для ебаного камня
        
        if self.brick_class==5: # Для евро, тут отключается ширина в выводе шаблона, и переопределяется вид
            t = Template(u'КЕ $view_d $mark $defect $refuse $features $tip')
            view=self.get_view()
        else:
            view=self.get_view()[:1] # Если обычный кирпич, то выводим Л(ицевой) и Р(ядовой)
        
        return t.substitute(weight_d = self.get_weight_display()[:1], # подставляем же! и возвращяем
                         view_d = view,
                         mark = self.get_mark_display(),
                         refuse = self.refuse,
                         defect = self.get_defect_display(),
                         features = self.features,
                         tip = self.get_color_type_display()
                         ).strip().replace('  ',' ')
    def get_absolute_url(self):
        return "/json/bricks/%i/" % self.id


    class Meta():
        ordering=['brick_class','-weight','-view','color_type','defect','refuse','mark','features','color']
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'


class brickForm(ModelForm):
    class Meta:
        model=bricks

#class BrickStore(Store):
##    id = StoreField()
#    brick_class    = StoreField()
#    color     = StoreField(get_value=ObjectMethod('get_color_display'))
#    mark     = StoreField(get_value=ObjectMethod('get_mark_display'))
#    view     = StoreField( get_value=ObjectMethod('get_view_display') )
#    weight     = StoreField( get_value=ObjectMethod('get_weight_display') )
#    color_type     = StoreField(get_value=ObjectMethod('get_color_type_display'))
#    refuse     = StoreField()
#    features     = StoreField()
#    defect     = StoreField()
#    total     = StoreField()
#
#    class Meta(object):
#        objects = bricks.objects.all()
##        label = bricks._meta.verbose_name
