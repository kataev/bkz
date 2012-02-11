# -*- coding: utf-8 -*-
__author__ = 'bteam'

def gdc(l):
    return l[0][0]


view=((u'Л',u'Лицевой'),(u'Р',u'Рядовой'))

weight=(
    (1.4,u'Утолщенный'),
    (1,u'Одинарный'),
    (0.8,u'Евро'),
    (2,u'Двойной'))

color=((0,u'Красный'),
                   (1,u'Желтый'),
                   (2,u'Коричневый'),
                   (3,u'Светлый'),
                   (4,u'Белый'))

brick_class_c=((0,u'Красный'),
                   (1,u'Желтый'),
                   (2,u'Коричневый'),
                   (3,u'Светлый'),
                   (4,u'Белый'),
                   (5,u'Евро'),
                   (6,u'Прочее'))

mark=((100,u'100'),
            (125,u'125'),
            (150,u'150'),
            (175,u'175'),
            (200,u'200'),
            (250,u'250'),
            (9000,u'брак'))

color_type=(('lyx','Без типа'),('1','1 тип'),('2','2 тип'),('3','3 тип'))
defect=((u'lyx',u'Люкс'),(u'<20',u'До 20%'),(u'>20',u'Более 20%'))
refuse=((u'no',u'Нет'),(u'Ф',u'Фаска'),(u'ФП',u'Фаска Полосы'),(u'ФФ',u'Фаска Фаска'),(u'ФФП',u'Фаска Фаска Полосы'),(u'П',u'Полосы'))

css_dict= dict(
    color=[u'bc-red',u'bc-yellow',u'bc-brown',u'bc-light',u'bc-white'],
    weight={1: u'single', 1.4: u'thickened', 2: u'double', 0.8:u'euro'},
    view={u'Л': u'facial', u'Р': u'common'},
    ctype={'': u'ctype-0', '1': u"ctype-1", '2': u'ctype-2', '3': u'ctype-3'},
    defect={u'': u'lux', u'<20': u'<20', u'>20': u'>20'},
    mark=0
)

def make_label(brick): # Говнокод для вывода имени
    if True:
#        t = Template(u'К$weight_d$view_dПу $mark $defect $refuse $features $tip') # Шаблон для обычного кирпича
        values = brick.__dict__.copy()
        values['weight']=brick.get_weight_display()
        values['mark']= unicode(brick.get_mark_display())
        values['color'] = brick.get_color_display()
        values['view'] = brick.get_view_display()
#        values['color_type']= self.get_color_type_display()
        template = u"К%(weight).1s%(view).1sПу %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s"

        if brick.weight == 2:
            template = u'КР %(mark)s %(color)s %(defect)s %(refuse)s %(features)s' # Шаблон для камня

        if brick.weight == 0.8:
            template = u'КЕ %(view)s %(mark)s %(color)s %(defect)s %(refuse)s %(features)s %(color_type)s'

        label = (template % values).strip().replace('  ',' ')
        return label


def make_css(brick):
    """ Метод для отображения стилей кирпича. """
    if True:
        css= u''
        for field,dict in css_dict.iteritems():
            val = getattr(brick,field,None)
            if field == 'mark':
                css+= u'mark-%d ' % val
                continue
            if field == 'color':
                css+= u'%s ' % dict[val]
            else:
                css+= u'%s ' % dict.get(val,'NOTFOUND'+field)
        css = css.strip()
        return css