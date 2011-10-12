# -*- coding: utf-8 -*-
from django.utils import unittest
from brick.models import Brick

class BrickTestCase(unittest.TestCase):
    def setUp(self):
        self.brick = Brick(1,1,100,u'1',u'Л',u'',u'',u'',u'',u'','test brick',1000)
        self.brick.save()

    def testUrl(self):
        self.assertEqual(self.brick.get_absolute_url(), '/brick/1/')

    def testUnique(self):
        self.bricks = map(lambda x:unicode(x),Brick.objects.all().order_by('id'))
        for b in self.bricks:
            self.assertEqual(self.bricks.count(b),1)

        

