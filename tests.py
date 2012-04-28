#!/usr/bin/env python
import unittest
import threading
from pool import WebPool
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class Tests(unittest.TestCase):

    wait = threading.Event().wait

    @classmethod
    def setUpClass(cls):
        cls.pool = WebPool()
        cls.brs = {'chrome': webdriver.Chrome,
                   'chrome1': webdriver.Chrome}
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
        self.assertIsInstance(ac['chrome1'], WebElement)
        self.assertIsInstance(ac['chrome'], WebElement)

    def test_go_to_links(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000')
        self.pool.action('get', 'http://localhost:8000/news/')

    def test_chain_actions(self):
        self.pool.start()
        self.pool.action('get', 'http://localhost:8000/feedback/')
        self.pool.action('find_element_by_name', 'name')
        self.pool.action('send_keys', 'None')
        vals = self.pool.result
        self.assertEquals(vals['chrome'].get_attribute('value'), 'None')
        self.assertEquals(vals['chrome1'].get_attribute('value'), 'None')

if __name__ == '__main__':
    unittest.main()
