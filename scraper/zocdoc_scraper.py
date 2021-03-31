import time
from scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from alerts import EmailAlerter

five_minutes = 60 * 5


class ZocdocScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.start_page = "https://www.zocdoc.com/vaccine/search/IL?flavor=state-search"
        self.alert_subject = "Vaccines available from Zocdoc?"
        self.alert_text = (
            f"Zocdoc may have appoints available. Visit {self.start_page} to check."
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
                time.sleep(five_minutes)
                raise e

    def navigate_eligibility(self):
        self.browser.get(self.start_page)

        try:
            self.get_element_by_xpath(
                '//button[@data-test="find-availability-button"]'
            ).click()
        except:
            self.browser.refresh()
            self.get_element_by_xpath(
                '//button[@data-test="find-availability-button"]'
            ).click()

        self.get_element_by_xpath('//input[@placeholder="Age"]').send_keys("29")
        self.get_element_by_xpath('//button[text()="Next"]').click()
        self.get_element_by_xpath(
            '//input[@name="healthcareWorker"][@value="N"]'
        ).click()
        self.get_element_by_xpath(
            '//input[@name="congregateWorker"][@value="N"]'
        ).click()
        self.get_element_by_xpath(
            '//input[@name="congregateWorker"][@value="N"]'
        ).click()
        self.get_element_by_xpath(
            '//input[@name="congregateResident"][@value="N"]'
        ).click()
        self.get_element_by_xpath('//button[@data-test="next-button"]').click()

        self.get_element_by_xpath(
            '//input[@name="essentialWorkerChicago"][@value="higherEducation"]'
        ).click()
        self.get_element_by_xpath('//button[@data-test="next-button"]').click()

        self.get_element_by_xpath('//input[@name="anaphylaxis"][@value="N"]').click()
        self.get_element_by_xpath('//input[@name="antibody"][@value="N"]').click()
        self.get_element_by_xpath(
            '//input[@name="recentVaccination"][@value="N"]'
        ).click()
        self.get_element_by_xpath(
            '//input[@name="recentVaccination"][@value="N"]'
        ).click()
        self.get_element_by_xpath(
            '//input[@name="recentDiagnosis"][@value="N"]'
        ).click()
        self.get_element_by_xpath('//button[@data-test="next-button"]').click()

    def navigate_appointments_form(self):

        self.get_element_by_xpath('//input[@data-test="checkbox-input"]').click()
        self.get_element_by_xpath(
            '//button[@data-test="see-availability-button"]'
        ).click()

    def alert_appointments_availability(self):
        appointments_available = self.get_element_by_xpath(
            '//button[@data-test="quick-links-availability-link"]', 5, True
        )

        if appointments_available is not None:
            self.alerter.send_alert()
        else:
            print("No Zocdoc alerts found")
