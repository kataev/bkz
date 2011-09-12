# -*- coding: utf-8 -*-
from django.db import models

class Brick(models.Model):
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
    
    def __unicode__(self): # Хитро выебаный код для вывода имени когда вызываем строку
#        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        values = self.__dict__
        values['weight']=self.get_weight_display()
        values['mark']= self.get_mark_display()
#        values['color_type']= self.get_color_type_display()
        template = u"К%(weight).1s%(view).1sПу %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s";

        if self.weight == u'Двойной':
            template = u'КР %(mark)s %(color)s %(defect)s %(refuse)s %(features)s' # Шаблон для ебаного камня

        if self.color==u'Кр':
            values['color'] = ''
        else:
            values['color'] = self.get_color_display()

        if self.brick_class==5 or self.brick_class==u'Евро': # Для евро, тут отключается ширина в выводе шаблона, и переопределяется вид
            template = u'КЕ %(view)s %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s'
            try:
                values['view']=self.euro_view[self.view]
            except :
                pass

        return (template % values).strip().replace('  ',' ')

    def get_absolute_url(self):
        return "/brick/%i/" % self.id

    def span(self):
        return u'<span class="'+self.show_css()+'">'+unicode(self)+'</span>'

    class Meta():
        ordering=['brick_class','-weight','-view','color_type','defect','refuse','mark','features','color']
        verbose_name = u"кирпич"
        verbose_name_plural = u'кирпичи'

    css={
        'view':{u'Л':u'facial',u'Р':u'common'},
        'weight':{u'1':u'single',u'1.4':u'thickened',u'2':u'double'},
        'color':{u'Кр':u'c_red',u'Же':u'c_ye',u'Ко':u'c_br',u'Св':u'c_li',u'Бе':u'wh'},
        'brick_class':{0:u'cl_red',1:u'cl_ye',2:u'cl_br',3:u'cl_li',4:u'cl_wh',5:u'cl_eu',6:u'cl_ot'},
        'mark':{100:u'm100',125:u'm125',150:u'm150',175:u'm175',200:u'm200',250:u'm250',9000:u'm9000'},
        'color_type':{'':u'type0','1':u"type1",'2':u'type2','3':u'type3'},
        'defect':{u'':u'lux',u'<20':u'p_20',u'>20':u'm_20'},
    }

    def show_css(self):
        css= u''

        for key in self.css.keys():
            try:
                prop = getattr(self,key)
                css+=u'%s ' % self.css[key][prop]
            except KeyError,e:
                pass
        return css.strip()
    
    class Admin:
        pass

class History(models.Model):
    brick = models.ForeignKey(Brick,verbose_name=u"Кирпич")
    date = models.DateField(u'Дата',auto_now_add=True)
    total = models.PositiveIntegerField(u"Остаток")

    def __unicode__(self):
        return u'%s от %s' % (self.brick,self.date)

    class Meta:
        verbose_name = u'История остатков кирпича'
        verbose_name_plural = verbose_name
        ordering = ('-date',)

class OldBrick(Brick):
    old_id = models.IntegerField('old id')

    class Admin:
        pass