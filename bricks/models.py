# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm,RadioSelect,DropDownSelect



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
    refuse_c=((u'',u''),(u'Ф',u'Фаска'),(u'ФП',u'Фаска Полосы'),(u'ФФ',u'Фаска Фаска'),(u'ФФП',u'Фаска Фаска Полосы'),(u'П',u'Полосы'))
           
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
#        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        values = self.__dict__
        values['weight']=self.get_weight_display()
        values['mark']= self.get_mark_display()
#        values['color_type']= self.get_color_type_display()
        template = u"К%(weight).1s%(view).1sПу %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s";

        if self.color==u'Кр':
            values['color'] = ''
        else:
            values['color'] = self.get_color_display()

        if self.weight==u'2':
            template = u'КР %(mark)s %(color)s %(defect)s %(refuse)s %(features)s' # Шаблон для ебаного камня
#
        if self.brick_class==5: # Для евро, тут отключается ширина в выводе шаблона, и переопределяется вид

            template = u'КЕ %(view)s %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s'
            try:
                values['view']=self.euro_view[self.view]
            except :
                pass
        return (template % values).strip().replace('  ',' ')
#                         mark = self.get_mark_display(),
#                         refuse = self.refuse,
#                         defect = self.get_defect_display(),
#                         features = self.features,
#                         tip = self.get_color_type_display()
#                         ).strip().replace('  ',' ')
    def get_absolute_url(self):
        return "/json/bricks/%i/" % self.id


    class Meta():
        ordering=['brick_class','-weight','-view','color_type','defect','refuse','mark','features','color']
        verbose_name = u"Кирпич"
        verbose_name_plural = u'Кирпичи'


    css={
        'view':{u'Л':u'facial',u'Р':u'common'},
        'weight':{u'1':u'single',u'1.4':u'thickened',u'2':u'double'},
        'color':{u'Кр':'c_red',u'Же':'c_ye',u'Ко':'c_br',u'Св':u'c_li',u'Бе':u'wh'},
        'brick_class':[u'cl_red',u'cl_ye',u'cl_br',u'cl_li',u'cl_wh',u'cl_eu',u'cl_ot',],
        'mark':{100:u'm100',125:u'm125',150:u'm150',175:u'm175',200:u'm200',250:u'm250',9000:u'm9000'},
        'color_type':{'':'type0','1':"type1",'2':'type2','3':'type3'},
        'defect':{u'':u'lux',u'<20':u'p_20',u'>20':u'm_20'},

    }

    def show_css(self):
        css= ''
        for key in self.css.keys():
            try:
                prop = getattr(self,key)
                css+='%s ' % self.css[key][prop]
            except :
                pass
        return css


class brickForm(ModelForm):
    class Meta:
        model=bricks

class brickSelectForm(ModelForm):
    class Meta:
        model=bricks
        exclude = ['total','name','features','color_type','refuse']
        widgets = {
            'color': RadioSelect(),
            'brick_class': RadioSelect(),
            'mark': RadioSelect(),
            'view': RadioSelect(),
            'weight': RadioSelect(),
            'defect': RadioSelect(),
        }

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
