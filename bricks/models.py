# -*- coding: utf-8 -*-
from django.db import models
from dojango.forms import ModelForm
from django.core.exceptions import ValidationError


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
            return self.euro_view[self.view] #Если евро, то подставляем в хитрый словарь
        
    
    def __unicode__(self): # Хитро выебаный код для вывода имени когда вызываем строку
        from string import Template # Шаблоны йоба
        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        
        if self.weight==u'2':
            t = Template(u'КР $mark $defect $refuse $features') # Шаблон для ебаного камня
        
        if self.brick_class==5: # Для евро, тут отключается ширина в выводе шаблона, и переопределяется вид
            t = Template(u'КЕ $view_d $mark $defect $refuse $features $tip')
            self.view=self.get_view()
        else:
            self.view=self.get_view()[:1] # Если обычный кирпич, то выводим Л(ицевой) и Р(ядовой)
        
        return t.substitute(weight_d = self.get_weight_display()[:1], # подставляем же! и возвращяем
                         view_d = self.view,
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


class brickForm(ModelForm):
    class Meta:
        model=bricks

#class oper(models.Model):
#    brick=models.ForeignKey(bricks,related_name="%(app_label)s_%(class)s_related",verbose_name=u"Кирпич",help_text=u'Выберите кирпич')
#    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Кол-во кирпича для операции')
#    time_change=models.DateTimeField(auto_now=True)
#    # DRAFT ДЛЯ ПРОСТОТЫ!!!! ПОДУМАТЬ!!!
#
#
#    class Meta:
#        abstract = True
#
#class doc(models.Model):
#
#    draft_c=((False,u'Чистовик'),(True,u'Черновик'))
#
#    number=models.PositiveIntegerField(unique=True,verbose_name=u'№ документа',help_text=u'Число')
#    doc_date=models.DateField(u'Дата',max_length=60,help_text=u'Дата документа')
#    info=models.CharField(u'Примечание',max_length=60,blank=True,help_text=u'Любая полезная информация')
#    time_change=models.DateTimeField(auto_now=True)
#    draft=models.BooleanField(u'Черновик',default=True,choices=draft_c,help_text=u'Если не черновик, то кирпич будет проводиться!')
#
#    class Meta:
#        abstract = True
#
#class transfer(models.Model):
#    brick_from=models.ForeignKey(bricks,related_name='from',verbose_name=u'Откуда',help_text=u'Из какого кирпича')
#    brick_to=models.ForeignKey(bricks,related_name='to',verbose_name=u'Куда',help_text=u'В какой')
#    amount=models.PositiveIntegerField(u"Кол-во",help_text=u'Число, больше остатка')
#    time_change=models.DateTimeField(auto_now=True)
#
#    def __unicode__(self):
#        return 0
#
#class transfer_form(ModelForm):
#    class Meta:
#        model=transfer
#
## Приход
#class arrival(oper):
#    pass
#    class Meta():
#            verbose_name = u"Приход"
#
#class arrival_form(ModelForm):
#    class Meta:
#        model=arrival
#
#
## Накладная
#class sold(oper):
#    price=models.DecimalField(u"Цена за единицу кирпича в Рублях",max_digits=8, decimal_places=4,help_text=u'Дробное число максимум 8символов в т.ч 4 после запятой')
#    delivery=models.DecimalField(u"Цена доставки",max_digits=6, decimal_places=3,blank=True,null=True,help_text=u'0 если доставки нет')
#    transfers = models.ManyToManyField(transfer,blank=True,null=True,help_text=u'Перевод для этой продажи')
#
#    class Meta():
#            verbose_name = u"Отгрузка"
#
#    #def __unicode__(self):
#    #    return u'id '+str(self.id)
#
#class sold_form(ModelForm):
#    class Meta:
#        model=sold
#
#class bills(doc):
#    solds = models.ManyToManyField(sold,blank=True,null=True,help_text=u'Отгрузки')
#    transfers = models.ManyToManyField(transfer,blank=True,null=True,help_text=u'Переводы') # НЕ НУЖЕН ПО ИДЕЕЕЕЕЕ!!!! Ведь солд и трансфер связаны m2m, их можно и так норм достать!
#
#    class Meta():
#            verbose_name = u"Накладная"
#
#class bills_form(ModelForm):
#    class Meta:
#        model=bills
#        widgets = {
#            'draft': CheckboxInput(attrs={'value': True})
#        }
#
#
#
##Списание
#class cons(oper):
#    pass
#
#
#class inventory(doc): # Инвентаризация
#    opers = models.ManyToManyField(cons,blank=True,null=True)
#    class Meta():
#            verbose_name = u"Инвенторизация"
#
#class inventory_form(ModelForm):
#    class Meta:
#        model=inventory
#
#
## Приход
#class coming(doc):
#    opers = models.ManyToManyField(arrival,blank=True,null=True)
#    class Meta():
#            verbose_name = u"Приход за день"
#
#class coming_form(ModelForm):
#    class Meta:
#        model=coming
