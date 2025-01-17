import unittest

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

from .common import *


class MonkeyTesting(unittest.TestCase):
    def test_random_click_student(self):
        # login normally
        driver.get(url)
        input_text(driver, "text", student_username)
        input_text(driver, "password", student_password)
        time.sleep(2)
        click_btn(driver, "loginbtn")
        time.sleep(2)
        for i in range(10000):
            links = []
            links.extend(driver.find_elements_by_tag_name("a"))
            links.extend(driver.find_elements_by_tag_name("Button"))
            links.extend(driver.find_elements_by_tag_name("button"))
            l = links[random.randint(0, len(links) - 1)]
            try:
                if not l.text == "Logout":
                    print(l.text)
                    l.click()
            except ElementNotInteractableException:  # when the attribute is not clickable
                continue
            except ElementClickInterceptedException:  # when the attribute is loading /changing
                continue
            time.sleep(1)

    def test_random_click_admin(self):
        # login normally
        driver.get(url)
        input_text(driver, "text", admin_username)
        input_text(driver, "password", admin_password)
        time.sleep(2)
        click_btn(driver, "loginbtn")
        time.sleep(2)
        for i in range(10000):
            links = []
            links.extend(driver.find_elements_by_tag_name("a"))
            links.extend(driver.find_elements_by_tag_name("Button"))
            links.extend(driver.find_elements_by_tag_name("button"))
            l = links[random.randint(0, len(links) - 1)]
            try:
                if not l.text == "Logout":
                    print(l.text)
                    l.click()
            except ElementNotInteractableException:  # when the attribute is not clickable
                continue
            except ElementClickInterceptedException:  # when the attribute is loading /changing
                continue
            time.sleep(1)
