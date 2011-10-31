# -*- coding: utf-8 -*-
__author__ = 'bteam'

euro_view={u'Л':u'УЛ',u'Р':u''} # Для имени

view_c=((u'Л',u'Лицевой'),(u'Р',u'Рядовой'))
weight_c=((u'1',u'Одинарный'),(u'1.4',u'Утолщенный'),(u'2',u'Двойной'))
color_c=((u'Кр',u'Красный'),
                   (u'Же',u'Желтый'),
                   (u'Ко',u'Коричневый'),
                   (u'Св',u'Светлый'),
                   (u'Бе',u'Белый'))

brick_class_c=((0,u'Красный'),
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

color_type_c=(('',''),('1','1 тип'),('2','2 тип'),('3','3 тип'))
defect_c=((u'',u''),(u'<20',u'До 20%'),(u'>20',u'Более 20%'))
refuse_c=((u'',u''),(u'Ф',u'Фаска'),(u'ФП',u'Фаска Полосы'),(u'ФФ',u'Фаска Фаска'),(u'ФФП',u'Фаска Фаска Полосы'),(u'П',u'Полосы'))

def make_label(brick): # Хитро код для вывода имени когда вызываем строку
    if True:
#        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        values = brick.__dict__
        values['weight']=brick.get_weight_display()
        values['mark']= unicode(brick.get_mark_display())
#        values['color_type']= self.get_color_type_display()
        template = u"К%(weight).1s%(view).1sПу %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s"

        if brick.weight == u'Двойной':
            template = u'КР %(mark)s %(color)s %(defect)s %(refuse)s %(features)s' # Шаблон для ебаного камня

        if brick.color==u'Кр':
            values['color'] = ''
        else:
            values['color'] = brick.get_color_display()

        if brick.brick_class==5 or brick.brick_class==u'Евро': # Для евро, тут отключается ширина в выводе шаблона, и переопределяется вид
            template = u'КЕ %(view)s %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s'
            try:
                values['view']=brick.euro_view[brick.view]
            except KeyError:
                pass
        brick.label = (template % values).strip().replace('  ',' ')
        brick.save()
        return brick


def make_css(brick):
    """ Метод для отображения стилей кирпича. """
    if True:
        css= u''
        for field,dict in brick.css_dict.iteritems():
            val = getattr(brick,field,None)
            css+= '%s ' % dict.get(val,'NOTFOUND'+field)
        brick.css = css.strip()
        brick.save()
        return brick