from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os


class Scraper:
    def __init__(self):
        pass

    @contextmanager
    def with_browser_session(self):
        option = webdriver.ChromeOptions()
        option.add_argument("--disable-blink-features=AutomationControlled")

        self.browser = webdriver.Chrome(options=option)
        self.browser.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        try:
            yield self.browser
        finally:
            self.browser.close()
            self.browser = None

    def get_element_by_xpath(self, xpath, wait_time=50, ignore_timeout=False):
        try:
            return WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            print("e", e)
            if ignore_timeout:
                return None
            raise e

    def get_element_by_css_selector(self, selector):
        return WebDriverWait(self.browser, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def get_element_by_name(self, name):
        return WebDriverWait(self.browser, 50).until(
            EC.presence_of_element_located((By.NAME, name))
        )
