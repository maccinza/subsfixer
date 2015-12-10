# -*- coding: utf-8 -*-
u"""

"""
import unittest
import os
import requests
import re
from selenium import webdriver
from datetime import datetime, timedelta

__author__ = 'infante'


def get_time_strings(content_string):
    time_regex = re.compile(r'\d{2}\:\d{2}:\d{2}')
    return list(time_regex.findall(content_string))


def compare_time_lists(original_list, converted_list, displacement):

    for _index, element in enumerate(original_list):
        time_obj = datetime.strptime(element, "%H:%M:%S")
        added_time = time_obj + timedelta(seconds=displacement)
        new_str_time = added_time.strftime("%H:%M:%S")
        if new_str_time != converted_list[_index]:
            return False
        return True


class SubsfixerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
        cls.file_name = 'original.srt'
        cls.seconds_displacement = '5'
        cls.invalid_file_name = 'invalid.inv'
        cls.invalid_content_file_name = 'invalid_content.srt'
        cls.invalid_displacement = 'invalid value'

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

    def test_empty_fields(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        (self.assertIn("Please, select a valid .srt file before submitting.", error_texts) and
         self.assertIn("Please, inform a valid value in seconds.", error_texts))

    def test_empty_displacement(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("file_placeholder").click()
        self.driver.find_element_by_id("subtitle_file").clear()
        self.driver.find_element_by_id("subtitle_file").\
            send_keys(os.path.join(self.fixtures_path, self.file_name))
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        file_input = self.driver.find_element_by_id("file_placeholder")
        (self.assertIn(self.file_name, file_input.get_attribute("data-content")) and
         self.assertIn("Please, inform a valid value in seconds.", error_texts))

    def test_empty_file(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("adjustment").send_keys(self.seconds_displacement)
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        (self.assertIn("Please, select a valid .srt file before submitting.", error_texts) and
         self.assertNotIn("Please, inform a valid value in seconds.", error_texts))

    def test_invalid_displacement(self):

        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("file_placeholder").click()
        self.driver.find_element_by_id("subtitle_file").clear()
        self.driver.find_element_by_id("subtitle_file").\
            send_keys(os.path.join(self.fixtures_path, self.file_name))

        self.driver.find_element_by_id("adjustment").send_keys(self.invalid_displacement)
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        self.assertIn("Please, inform a valid value in seconds.", error_texts)

    def test_invalid_file_extension(self):
        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("file_placeholder").click()
        self.driver.find_element_by_id("subtitle_file").clear()
        self.driver.find_element_by_id("subtitle_file").\
            send_keys(os.path.join(self.fixtures_path, self.invalid_file_name))
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        self.assertIn("Please, select a valid .srt file before submitting.", error_texts)

    def test_invalid_content(self):

        self.driver.get('http://localhost:5000')

        submit_button = self.driver.find_element_by_css_selector("#submit")

        self.driver.find_element_by_id("file_placeholder").click()
        self.driver.find_element_by_id("subtitle_file").clear()
        self.driver.find_element_by_id("subtitle_file").\
            send_keys(os.path.join(self.fixtures_path, self.invalid_content_file_name))

        self.driver.find_element_by_id("adjustment").send_keys(self.seconds_displacement)
        submit_button.click()

        errors = self.driver.find_elements_by_css_selector(".form-error")
        error_texts = [e.text for e in errors]

        self.assertIn("File is not in the expected format and/or does not contain expected content.", error_texts)

    def test_successfull_submission(self):

        _file = open(os.path.join(self.fixtures_path, self.file_name), 'rb')
        original_content = _file.read()
        _file.close()

        payload = {
            'adjustment': self.seconds_displacement
        }

        files = {'subtitle_file': open(os.path.join(self.fixtures_path, self.file_name), 'rb')}

        response = requests.post('http://localhost:5000', data=payload, files=files)

        fixed_content = response.content

        original_times = get_time_strings(original_content)
        fixed_times = get_time_strings(fixed_content)

        are_the_same = compare_time_lists(original_times, fixed_times, int(self.seconds_displacement))
        self.assertTrue(are_the_same)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
