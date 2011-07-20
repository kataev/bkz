from whs.bricks.models import bricks

for a in bricks.objects.filter(weight=u'2'):
    print a.pk,a,a.weight,a.name

