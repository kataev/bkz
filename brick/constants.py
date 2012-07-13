# -*- coding: utf-8 -*-
__author__ = 'bteam'

poddon_c = ((288, u'Маленький поддон'), (352, u'Обычный поддон'))

BrickOrder = ('-width', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')

view_c = ((u'Л', u'Лицевой'), (u'Р', u'Рядовой'))

width_c = (
    (1.4, u'Утолщенный'),
    (1.0, u'Одинарный'),
    (0.8, u'Евро'),
    (0.0, u'Двойной'),
    )

mass_c = {1.4: 3.5,
         1.0: 2.5,
         0.8: 2.5,
         0.0: 5.0
}

cavitation_c = ((0, u'Пустотелый'),
           (1, u'Полнотелый'),
)

color_c = ((0, u'Красный'),
         (1, u'Желтый'),
         (2, u'Коричневый'),
         (3, u'Светлый'),
         (4, u'Белый'))

mark_c = ((100, u'100'),
        (125, u'125'),
        (150, u'150'),
        (175, u'175'),
        (200, u'200'),
        (250, u'250'),
        (300, u'300'),
        (9000, u'брак'))

color_type_c = (('', 'Без типа'), ('1', 'тип 1'), ('2', 'тип 2'), ('3', 'тип 3'))
defect_c = ((u'', u'Гост'), (u'<20', u'До 20%'), (u'>20', u'Более 20%'))
refuse_c = (
(u'', u'Нет'), (u'Ф', u'Фаска'), (u'ФП', u'Фаска Полосы'), (u'ФФ', u'Фаска Фаска'), (u'ФФП', u'Фаска Фаска Полосы'),
(u'П', u'Полосы'))

css_dict = dict(
    color=[u'bc-red', u'bc-yellow', u'bc-brown', u'bc-light', u'bc-white'],
    width={1: u'w-single', 1.4: u'w-thickened', 0: u'w-double', 0.8: u'w-euro'},
    view={u'Л': u'v-facial', u'Р': u'v-common'},
    ctype={'': u'ctype-0', '1': u"ctype-1", '2': u'ctype-2', '3': u'ctype-3'},
    defect={u'': u'd-lux', u'<20': u'd-l20', u'>20': u'd-g20'},
    mark=0,
    features=0
)

def get_name(brick):
    if brick.width == 0.8:
        if brick.view == u'Л':
            return u'КЕ УЛ'
        if brick.view == u'Р':
            return u'КЕ'
    elif brick.width == 0:
        return u'КР'
    else:
        if brick.cavitation:
            c = u'о'
        else:
            c = u'у'
        return u'К<b>%s</b>%sП%s' % (brick.get_width_display()[0], brick.view,c)


def make_label(brick): # Код для вывода имени
    label = get_name(brick) + ' %s' % brick.get_mark_display()
    if brick.color:
        label += ' %s' % brick.get_color_display()
    if brick.ctype:
        label += ' %s' % brick.get_ctype_display()
    if brick.defect:
        label += ' %s' % brick.defect
    if brick.features:
        label += ' %s' % brick.features.lower()
    if brick.refuse:
        label += ' %s' % brick.refuse
    return label


def make_css(brick):
    """ Метод для отображения стилей кирпича. """
    css = u''
    for field, dict in css_dict.iteritems():
        val = getattr(brick, field, None)
        if field == 'mark':
            css += u'mark-%d ' % val
        elif field == 'color':
            css += u'%s ' % dict[val]
        elif field == 'defect':
            css += u'%s ' % dict[val]
        elif field == 'features':
            if not brick.features and brick.mark <= 1000 and not brick.defect: css += u'nofeatures '
            else: css += u'features '
        else:
            css += u'%s ' % dict.get(val, 'NOTFOUND' + field)
    css = css.strip()
    return css