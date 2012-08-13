#!/usr/bin/env python
import unittest
import threading

from pool import WebPool

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


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
                   'chrome1': webdriver.Chrome,
                   'chrome2': webdriver.Chrome}
        cls.pool.browsers = cls.brs
        cls.pool.action('implicitly_wait', 40)

    @classmethod
    def tearDownClass(cls):
        cls.pool.stop()

    def test_add_browser(self):
        self.assertEquals(self.pool.browsers, self.brs)

    def test_get_page_browsers(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000')
        self.pool.action('find_element_by_tag_name', 'p')

        check_item(result=self.pool.result, assertion=self.assertIsInstance, arg=WebElement)
        check(result=self.pool.result, assertion=self.assertEquals, act='tag_name', arg='p')

    def test_go_to_links(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000')
        self.pool.action('get', 'http://localhost:8000/news/')

        check(result=self.pool.browsers, assertion=self.assertEquals,
              act='current_url', arg=u'http://localhost:8000/news/')

    def test_chain_actions(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000/feedback/')
        self.pool.action('find_element_by_name', 'name')
        self.pool.action('send_keys', 'None')

        check(result=self.pool.result, assertion=self.assertEquals,
              act=('get_attribute', 'value'), arg='None')

    def test_login(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8001')
        self.pool.action('find_element_by_name', "login")
        self.pool.action('send_keys', u"root\ue004")
        self.pool.action('find_element_by_name', "password")
        self.pool.action('send_keys', u"root\ue007")
        self.pool.action('find_element_by_css_selector', '.langs-streams a[href="/news/"]')
        self.pool.action('click')

        check(result=self.pool.browsers, assertion=self.assertEquals,
              act='current_url', arg=u'http://localhost:8001/news/')


class TestPool(unittest.TestCase):
    def setUp(self):
        self.pool = WebPool()

    def test_object(self):
        self.assertIsInstance(self.pool, WebPool)

    def test_empty(self):
        self.assertDictEqual(self.pool.browsers, {})
        self.assertDictEqual(self.pool.result, {})
        self.assertDictEqual(self.pool.actions, {})
        self.assertEquals(self.pool.ignored, ('send_keys', 'get'))

    def test_start(self):
        self.pool.start()
        brs = {'chrome': webdriver.Chrome,
               'chrome1': webdriver.Chrome,
               'chrome2': webdriver.Chrome}
        self.pool.browsers = brs
        self.assertEquals(self.pool.browsers.keys(), ['chrome', 'chrome1', 'chrome2'])
        self.pool.start()
        self.assertEquals(self.pool.result.keys(), ['chrome', 'chrome1', 'chrome2'])
        self.pool.stop()
        self.assertDictEqual(self.pool.result, {})


if __name__ == '__main__':
    unittest.main()
