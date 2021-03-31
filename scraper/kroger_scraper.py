import time
from scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from alerts import EmailAlerter

two_minutes = 60 * 2


class KrogerScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.start_page = "https://www.kroger.com/rx/covid-eligibility"
        self.alert_subject = "Vaccines available from Kroger?"
        self.alert_text = (
            f"Kroger may have appoints available. Visit {self.start_page} to check."
        )
        self.alerter = EmailAlerter(self.alert_subject, self.alert_text)

    def scrape(self):
        with self.with_browser_session() as browser:
            try:
                self.navigate_eligibility()
                self.navigate_appointments_form()
                self.alert_appointments_availability()
            except Exception as e:
                print(
                    "Error navigating page. Timing out for awhile to try to manually pass CAPTCHA"
                )
                time.sleep(two_minutes)
                raise e

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

    def navigate_eligibility(self):

        self.browser.get(self.start_page)
        self.get_element_by_xpath('//button[text()="I Agree"]').click()
        self.get_element_by_xpath('//button[text()="No"]').click()
        state_select = Select(self.get_element_by_css_selector("select.kds-Select"))
        state_select.select_by_visible_text("IL")
        dob_input = self.get_element_by_name("Date of Birth")
        dob_input.send_keys("03/11/1992")
        self.get_element_by_xpath('//button[text()="Submit"]').click()
        no_first_dose_button = self.get_element_by_xpath(
            '//div[not(contains(@class, "not-allowed"))]/button[text()="No"]'
        )
        no_first_dose_button.click()
        no_recent_vaccine_button = self.get_element_by_xpath(
            '//div[not(contains(@class, "not-allowed"))]/button[text()="No"]'
        )
        no_recent_vaccine_button.click()
        occupation_select = Select(
            self.get_element_by_css_selector("select.kds-Select:not([disabled])")
        )
        occupation_select.select_by_visible_text("Higher Education Worker")
        self.get_element_by_xpath(
            '//button[text()="Schedule Your COVID-19 Vaccine"]'
        ).click()

    def navigate_appointments_form(self):
        self.get_element_by_xpath(
            '//input[@placeholder="ZIP Code or City, State"]'
        ).send_keys("60657")
        distance_select = Select(
            self.get_element_by_css_selector("select.kds-Select:not([disabled])")
        )
        distance_select.select_by_visible_text("5 miles")
        find_appointment_button = self.get_element_by_xpath(
            '//button[text()="Find Appointment"]'
        )
        find_appointment_button.click()

    def alert_appointments_availability(self):
        no_appointments_alert = self.get_element_by_xpath(
            '//span[contains(text(), "None of the locations in your search")]', 5, True
        )

        if no_appointments_alert is None:
            self.alerter.send_alert()
        else:
            print("No Kroger alerts found")
