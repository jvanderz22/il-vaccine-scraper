import time
from datetime import datetime, timedelta
from kroger_scraper import KrogerScraper
from zocdoc_scraper import ZocdocScraper

five_minutes = 60 * 5
if __name__ == "__main__":
    kroger_scraper = KrogerScraper()
    zocdoc_scraper = ZocdocScraper()
    kroger_sleep_until = None
    zocdoc_sleep_until = None
    while True:
        cur_time = datetime.now()
        if kroger_sleep_until is None or kroger_sleep_until < cur_time:
            try:
                kroger_scraper.scrape()
            except:
                kroger_sleep_until = cur_time + timedelta(hours=1)
                print(
                    f"caught kroger scraper error. Wait until {kroger_sleep_until} to try again"
                )

        cur_time = datetime.now()
        if zocdoc_sleep_until is None or zocdoc_sleep_until < cur_time:
            try:
                zocdoc_scraper.scrape()
            except:
                zocdoc_sleep_until = cur_time + timedelta(minutes=10)
                print(
                    f"caught zocdoc scraper error. Wait until {zocdoc_sleep_until} to try again"
                )

        time.sleep(five_minutes)
