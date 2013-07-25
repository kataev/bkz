# -*- coding: utf-8 -*-
import re

__author__ = 'bteam'
from collections import OrderedDict

poddon_c = ((288, u'Маленький поддон'), (352, u'Обычный поддон'))

BrickOrder = ('width', 'color', '-view', 'ctype', '-defect', '-features__name', 'mark', 'refuse', 'id')

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

cad_c = (
    (0.8, u'Высокой эффективности'),
    (1.0, u'Повышенной эффективности'),
    (1.2, u'Эффективный'),
    (1.4, u'Условно-эффективный'),
    (2.0, u'Малоэффективные')
)

frostresistance_c = (
    (25, u'F25'),
    (35, u'F35'),
    (50, u'F50'),
    (75, u'F75'),
    (100, u'F100'),
)

ctype_c = (('0', 'Без типа'), ('1', 'тип 1'), ('2', 'тип 2'), ('3', 'тип 3'))
defect_c = ((u'gost', u'Гост'), (u'<20', u'До 20%'), (u'>20', u'Более 20%'), (u'no_cont', u'Некондиция'))
refuse_c = (
    (u'', u'Нет'), (u'Ф', u'Фаска'), (u'ФП', u'Фаска Полосы'), (u'ФФ', u'Фаска Фаска'), (u'ФФП', u'Фаска Фаска Полосы'),
    (u'П', u'Полосы'))

css_dict = OrderedDict()
css_dict['color'] = {0: u'bc-red', 1: u'bc-yellow', 2: u'bc-brown', 3: u'bc-light', 4: u'bc-white'}
css_dict['width'] = {2: u'w-single', 1: u'w-thickened', 4: u'w-double', 3: u'w-euro'}
css_dict['view'] = {u'Л': u'v-facial', u'Р': u'v-common'}
css_dict['mark'] = {100: 'mark-100', 125: 'mark-125', 150: 'mark-150', 175: 'mark-175',
                    200: 'mark-200', 250: 'mark-250', 300: 'mark-300', 9000: 'mark-9000'}
css_dict['defect'] = {u'gost': u'd-lux', u'<20': u'd-l20', u'>20': u'd-g20', u'no_cont': u'g-no'}
css_dict['ctype'] = {'0': u'ctype-0', '1': u"ctype-1", '2': u'ctype-2', '3': u'ctype-3'}
css_dict['features'] = {}

from django.db.models import get_model


def get_menu(css_dict=css_dict):
    Brick = get_model('whs', 'brick')
    result = []
    for name, items in css_dict.iteritems():
        field = Brick._meta.get_field_by_name(name)[0]
        choices = field.get_choices()
        print choices
        o = dict(verbose_name=field.verbose_name)
        if name == 'features':
            continue
        o['name'] = name
        o['items'] = [(css_dict[name][k], v) for k, v in field.get_choices() if k != '']
        result.append(o)
    return result


def get_name(self):
    name = self.width.label + getattr(self, 'view', u'Р') + u'П' + (self.get_cavitation_display()[1:2]).lower()
    return name


def get_full_name(self):
    name = u'%s ' % get_name(self)
    if not self.mark == 9000:
        name += '/'.join(unicode(s) for s in (self.width.value, self.mark or '?', self.cad or u'?'))

    if self.frost_resistance:
        name += u'/%s ' % self.frost_resistance.value
    else:
        name += '/? '

    if hasattr(self, 'defect') and self.defect == u'gost':
        name += u' ГОСТ 530-2007 '
    if self.color:
        name += self.get_color_display()
    return name


def make_label(brick): # Функция для вывода имени
    label = get_name(brick) + ' %s' % brick.get_mark_display()
    if brick.color:
        label += ' %s' % brick.get_color_display()
    if brick.ctype and int(brick.ctype):
        label += ' %s' % brick.get_ctype_display()
    if brick.defect and not brick.defect == 'gost':
        label += ' %s' % brick.defect
    if brick.features:
        label += ' ' + ' '.join([f[0] for f in brick.features.values_list('name')])
    if brick.refuse:
        label += ' %s' % brick.refuse
    return re.sub(' +', ' ', label)


def make_css(brick):
    """ Метод для отображения стилей кирпича. """
    css = u''
    for field, dict in css_dict.iteritems():
        val = getattr(brick, field, None)
        if hasattr(val, 'pk'):
            val = getattr(brick, field + '_id', None)
        if field == 'mark':
            css += u'mark-%d ' % val
        elif field == 'color':
            css += u'%s ' % dict[val]
        elif field == 'defect':
            css += u'%s ' % dict[val]
        elif field == 'features':
            if not brick.features and brick.mark <= 1000 and not brick.defect:
                css += u'nofeatures '
            else:
                css += u'features '
        else:
            css += u'%s ' % dict.get(val, 'NOTFOUND' + field)
    css = css.strip()
    return css


def bricks_per_pallet(brick):
    if brick.width == 4:
        return 160
    if brick.color == 1:
        if brick.width_id == 1:
            return 192
        else:
            return 264
    if brick.view == u'Р':
        if brick.width_id == 1:
            return 288
        elif brick.width_id == 2:
            return 352
        elif brick.width_id == 3:
            return 352
    else:
        if brick.width_id == 1:
            return 192
        elif brick.width_id == 2:
            return 264
        elif brick.width_id == 3:
            return 256

