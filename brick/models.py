# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Brick(models.Model):
    """
    Класс для кирпича, основа приложения, выделен в отдельный блок.
    Содержит информацию о характеристиках кирпича и текушем остатке

    """
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
            (9000,u'брак'))
    
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
    features=models.CharField(u"Редкие особенности",max_length=60,blank=True,help_text=u'Oттенки, тычки и прочее')
    name=models.CharField(u"Имя",max_length=160,default='')
    total=models.PositiveIntegerField(u"Текуший остаток",default=0)

    css=models.CharField(u"Css",max_length=360,default=u'')
    label=models.CharField(u"ИмяЯ",max_length=660,default='')

    def __unicode__(self):
        if not self.pk:
            return u'Новый кирпич'
        else:
            return self.label

    def make_label(self): # Хитро код для вывода имени когда вызываем строку
#        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        values = self.__dict__
        values['weight']=self.get_weight_display()
        values['mark']= unicode(self.get_mark_display())
#        values['color_type']= self.get_color_type_display()
        template = u"К%(weight).1s%(view).1sПу %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s"

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
            except KeyError:
                pass

        return (template % values).strip().replace('  ',' ')

    def get_absolute_url(self):
        return "/brick/%i/" % self.id

    class Meta():
        ordering=['brick_class','-weight','-view','color_type','defect','refuse','mark','features','color']
        verbose_name = u"кирпич"
        verbose_name_plural = u'кирпичи'

    css_dict={
        'view':{u'Л':u'facial',u'Р':u'common'},
        'weight':{u'1':u'single',u'1.4':u'thickened',u'2':u'double'},
#        'color':{u'Кр':u'c_red',u'Же':u'c_ye',u'Ко':u'c_br',u'Св':u'c_li',u'Бе':u'wh'},
        'brick_class':{0:u'cl_red',1:u'cl_ye',2:u'cl_br',3:u'cl_li',4:u'cl_wh',5:u'cl_eu',6:u'cl_ot'},
        'mark':{100:u'm100',125:u'm125',150:u'm150',175:u'm175',200:u'm200',250:u'm250',9000:u'm9000'},
        'color_type':{'':u'type0','1':u"type1",'2':u'type2','3':u'type3'},
        'defect':{u'':u'lux',u'<20':u'p_20',u'>20':u'm_20'},
    }

    def make_css(self):
        """
        Метод для отображения стилей кирпича.
        """
        css= u''
        for field,dict in self.css_dict.iteritems():
            val = getattr(self,field,None)
            css+= '%s ' % dict.get(val,'NOTFOUND'+field)
        return css.strip()

class BrickTable(Brick):
    """
    Абстракная модель, наследованая от кирпича. Не содержит данных,
    Необходима для представления, чтобы на нее навешивать данные
    посчитанные при обработке запроса.
    """
    begin=models.PositiveIntegerField(u"Начало месяца",default=0)
    plus=models.PositiveIntegerField(u"Приход",default=0)
    t_from=models.PositiveIntegerField(u"Перевод из",default=0)
    t_to=models.PositiveIntegerField(u"Перевод в",default=0)
    sold=models.PositiveIntegerField(u"Отгрузка",default=0)

    class Meta:
        abstract = True

class OldBrick(Brick):
    old_id= models.IntegerField('old id')