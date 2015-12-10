# -*- coding: utf-8 -*-
u"""

"""
import unittest
from selenium import webdriver
from server import app

if app.debug:
    from dev_config import TESTS
else:
    from config import TESTS

__author__ = 'infante'


class SubsfixerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    def test_welcome_msg(self):
        self.driver.get('http://localhost:5000')

        welcome_msg = self.driver.find_element_by_css_selector(".app-hint>p").text
        self.assertEqual(welcome_msg, "Welcome!")

    def test_form_exists(self):
        self.driver.get('http://localhost:5000')

        subs_form = self.driver.find_element_by_css_selector("#subtitle_form")
        self.assertIsNotNone(subs_form)

        file_input = self.driver.find_element_by_css_selector("#file_placeholder")
        self.assertEqual(file_input.get_attribute("data-content"), "Choose your .srt file...")

        displ_input = self.driver.find_element_by_css_selector("#file_placeholder")
        self.assertIsNone(displ_input.get_attribute("value"))

    def test_form_all_fields_empty(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        (self.assertIn("Please, select a valid .srt file before submitting.", error_texts) and
         self.assertIn("Please, inform a valid value in seconds.", error_texts))

    def test_seconds_empty(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("file_placeholder").click()
        self.driver.find_element_by_id("subtitle_file").clear()
        self.driver.find_element_by_id("subtitle_file").\
            send_keys(TESTS['file_path'])
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        file_input = self.driver.find_element_by_id("file_placeholder")
        (self.assertIn(TESTS['file_name'], file_input.get_attribute("data-content")) and
         self.assertIn("Please, inform a valid value in seconds.", error_texts))

    def test_file_empty(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("adjustment").send_keys("5")
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        (self.assertIn("Please, select a valid .srt file before submitting.", error_texts) and
         self.assertNotIn("Please, inform a valid value in seconds.", error_texts))

    # TODO: test successful submission and download

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
