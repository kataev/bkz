# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase,TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from whs.brick.models import Brick
from whs.brick.constants import *


class BrickTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_Brick_via_admin_site(self):
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(u'Администрирование Django', body.text)

        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # her username and password are accepted, and she is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(u'Администрирование сайта', body.text)

        # She now sees a couple of hyperlink that says "Bricks"
        Bricks_links = self.browser.find_elements_by_link_text('Bricks')
        self.assertEquals(len(Bricks_links), 2)

        # TODO: Gertrude uses the admin site to create a new Brick
        self.fail('todo: finish tests')


class BrickModelTest(TestCase):
    def test_creating_a_new_brick_and_saving_it_to_the_database(self):
        # start by creating a new Brick object with its "question" set
        brick = Brick()
        brick.save()

        # now check we can find it in the database again
        all_bricks_in_database = Brick.objects.all()
        self.assertEquals(len(all_bricks_in_database), 1)
        only_brick_in_database = all_bricks_in_database[0]
        self.assertEquals(only_brick_in_database, Brick)