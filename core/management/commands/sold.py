# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from bkz.whs.models import *
from bkz.lab.models import *
from bkz.old.models import *
from random import randint
class Command(BaseCommand):
	help = "Commands for lagasy db"
	def handle(self, *args, **options):
		self.totals()

	def totals(self):
		for b in Bill.objects.all():
			for i in range(randint(1,3)):
				b1=Brick.objects.filter(mark__lt=250,color__lt=3).order_by('?')[0]
				s = Sold(doc=b,brick=b1)
				if b1.mark > 100 and randint(0,10) > 7:
					b2 = Brick.objects.filter(color=b1.color,width=b1.width,mark__gte=b1.mark).order_by('?')
					if b2:
						s.brick_from=b2[0]
				s.tara = randint(6,18)
				s.amount = s.brick.get_bricks_per_pallet * s.tara
				if s.brick.color == 0:
					if s.brick.view == u'Р':
						if s.brick.width_id == 1:
							if s.brick.mark == 100: 
								s.price = 8.60
							elif s.brick.mark == 125:
 								s.price = 9
							elif s.brick.mark == 150: 
								s.price = 9.4
							elif s.brick.mark == 175: 
								s.price = 9.8
							else: 
								s.price = 10.20
						if s.brick.width_id == 2:
							if s.brick.mark == 100: s.price = 6.50
							elif s.brick.mark == 125: s.price = 6.80
							elif s.brick.mark == 150: s.price = 7.20
							elif s.brick.mark == 175: s.price = 7.60
							elif s.brick.mark >= 200: s.price = 8.00
						else:
							s.price = 6.8
					else:
						if s.brick.width_id == 1:
							s.price = 12.6
						if s.brick.width_id == 2:
							s.price = 10
						else:
							s.price = 6.8

				if s.brick.color == 1:
					if s.brick.view == u'Р':
						if s.brick.width_id == 1:
							s.price = 11.8
						if s.brick.width_id == 2:
							s.price = 10.5
						else:
							s.price = 12
					else:
						if s.brick.width_id == 1:
							s.price = 11.8
						if s.brick.width_id == 2:
							s.price = 10.5
						else:
							s.price = 15.8
				if s.brick.color == 2:
					if s.brick.view == u'Р':
						if s.brick.width_id == 1:
							s.price = 11.8
						if s.brick.width_id == 2:
							s.price = 10.5
						else:
							s.price = 12
					else:
						if s.brick.width_id == 1:
							s.price = 11.8
						if s.brick.width_id == 2:
							s.price = 10.5
						else:
							s.price = 15.8
				s.save()
			if randint(0,10) > 7:
				p = Pallet(doc=b,amount=sum([s.tara for s in b.solds.all()]))
				p.save()

