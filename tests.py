#!/usr/bin/env python
import unittest
import threading
from pool import WebPool
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def check(result=None, assertion=None, act=None, arg=None):
    for name, value in result.items():
        if isinstance(act, (tuple, list)):
            assertion(getattr(value, act[0])(act[1]), arg)
        else:
            assertion(getattr(value, act), arg)


def check_item(result=None, assertion=None, arg=None):
    for name, value in result.items():
        assertion(value, arg)


class Tests(unittest.TestCase):

    wait = threading.Event().wait

    @classmethod
    def setUpClass(cls):
        cls.pool = WebPool()
        cls.brs = {'chrome': webdriver.Chrome,
                   'firefox': webdriver.Firefox}
        cls.pool.browsers = cls.brs
        cls.pool.action('implicitly_wait', 40)

    @classmethod
    def tearDownClass(cls):
        cls.pool.stop()
        cls.pool.result = {}

    def test_add_browser(self):
        self.assertEquals(self.pool.browsers, self.brs)

    def test_get_page_browsers(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000')
        ac = self.pool.action('find_element_by_tag_name', 'p')

        check_item(result=ac, assertion=self.assertIsInstance, arg=WebElement)
        check(result=ac, assertion=self.assertEquals, act='tag_name', arg='p')

    def test_go_to_links(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000')
        ac = self.pool.action('get', 'http://localhost:8000/news/')

        check(result=ac, assertion=self.assertEquals,
              act='current_url', arg=u'http://localhost:8000/news/')

    def test_chain_actions(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000/feedback/')
        self.pool.action('find_element_by_name', 'name')
        vals = self.pool.action('send_keys', 'None')

        check(result=vals, assertion=self.assertEquals,
              act=('get_attribute', 'value'), arg='None')

if __name__ == '__main__':
    unittest.main()
