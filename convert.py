# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django.utils import simplejson
from brick.models import Brick
from django.core.exceptions import ValidationError

json = simplejson.loads(file('bricks.json').readline())

example = {'brick_class': 0,
           'color': u'\u041a\u0440',
           'color_type': '',
           'css': 'thickened type0 lux m100 cl_red common',
           'defect': '',
           'features': '',
           'label': u'\u041a\u0423\u0420\u041f\u0443 100  \u0424',
           'mark': 100,
           'name': u'\u041a\u0423\u0420\u041f\u0443 1,4 \u041d\u0424/100/1,4/50/ \u0413\u041e\u0421\u0422 530-2007 \u0444 ',
           'refuse': u'\u0424',
           'total': 794,
           'view': u'\u0420',
           'weight': '1.4'}
color_c=((u'Кр',u'Красный'),
         (u'Же',u'Желтый'),
         (u'Ко',u'Коричневый'),
         (u'Св',u'Светлый'),
         (u'Бе',u'Белый'))
def from_ajax_to_boot():
    for b in json:
        brick = Brick()
        brick.pk = b['pk']
        f = b['fields']
        if f['brick_class']>4:
            if f['brick_class']==6:
                brick.weight = 2
            if f['brick_class']==5:
                brick.weight = 0.8
            try:
                brick.color = map(lambda x: x[1],color_c).index(f['color'])
            except ValueError:
                brick.color = 1

            if f['view'] == u'\u0423\u041b':
                brick.view = u'Л'
            else:
                brick.view = u'Р'
        else:
            brick.weight = float(f['weight'])
            brick.color = f['brick_class']
            brick.view = f['view']

        brick.mark = f['mark']

        brick.ctype = f['color_type']
        brick.defect = f['defect']
        brick.refuse = f['refuse']
        brick.features = f['features']
        brick.name = f['name']
        brick.css = f['css']
        brick.label = f['label']
        try:
            brick.full_clean()
        except ValidationError,e:
    #        print f

            for m in e.message_dict:
                print m,e.message_dict[m][0]
        brick.save()

if __name__ == '__main__':
    from_ajax_to_boot()