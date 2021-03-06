import sys
from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as exp_con
import selenium.webdriver.support.ui as ui
import pandas as pd
import urllib.request

from exceptions import *


class GoogleMapsCrawler:

    def __init__(self, target, results_per_page, no_pages):
        self.DRIVER_TITLE = target
        self.NO_RESULTS = results_per_page
        self.NO_PAGES = no_pages
        self.data = []
        self.times_printed = 1

    def is_connected_to_network(self):
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False

    def wait_for_reconnection(self):
        not_connected = True
        ten_minutes = 10 * 60  # 10 times 60 seconds
        time_elapsed = 0
        while not_connected:
            if time_elapsed > ten_minutes:
                raise NetworkConnectionException
            sleep(3)
            time_elapsed += (3 + 1)  # 3 seconds on sleep, another 1 for other calculations
            not_connected = not self.is_connected_to_network()

    def get_url(self, to_search):
        url_fragment = to_search.replace(' ', '+')
        return 'https://www.google.com/maps/search/' + url_fragment

    def get_waiter(self, driver, timeout=10):
        return ui.WebDriverWait(driver, timeout)

    def export_to_csv(self):
        data_frame = pd.DataFrame(self.data, columns=['name', 'contact number', 'address1', 'address2', 'website'])
        print('the data frame contains', len(self.data), 'rows.')
        file_name = self.DRIVER_TITLE.replace(' ', '_') + '-' + str(self.times_printed)+'.csv'
        data_frame.to_csv(file_name)

    def scrape_results(self, driver, curr_page):
        wait = self.get_waiter(driver)  # init waiter for this method
        print('{}th page'.format(curr_page))
        # i had to do this because google chrome seems to have a weird behaviour
        for curr_item in range(self.NO_RESULTS):
            sys.stdout.write('{}th iteration\r'.format(curr_item))
            sys.stdout.flush()
            for page in range((curr_page-1)):
                try:
                    next_button = driver.find_element(By.XPATH, '//div/button[contains(@aria-label,"Next page")]')
                except Exception:
                    wait.until(exp_con.visibility_of_element_located((
                        By.XPATH, '//div/button[contains(@aria-label,"Next page")]'
                    )))
                    next_button = driver.find_element(By.XPATH, '//div/button[contains(@aria-label,"Next page")]')
                if next_button.is_enabled():
                    sleep(1)
                    wait.until(exp_con.element_to_be_clickable((
                        By.XPATH, '//div/button[contains(@aria-label,"Next page")]'
                    )))
                    # FIXME: Here on next_button.click(), ElementClickInterceptedException is being raised when there's
                    # FIXME:  a problem with the element.
                    # TODO: I used another way of clicking the next button. please check
                    try:
                        next_button.click()
                    except Exception:
                        try:
                            # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen#answer-48667924
                            print('ElementClickInterceptedException occurred. trying a click workaround.')
                            webdriver.ActionChains(driver).move_to_element(next_button).click(next_button).perform()
                        except Exception:
                            raise StaleElementException
                try:
                    wait.until(
                        exp_con.presence_of_element_located((
                            By.XPATH, '//div[@class="section-result"]'
                        ))
                    )
                    sleep(2)
                except Exception:
                    try:
                        wait.until(
                            exp_con.presence_of_element_located((
                                By.XPATH, '//div[@class="section-result"]'
                            ))
                        )
                    except Exception:
                        self.export_to_csv()
                        pass
            results = driver.find_elements(By.XPATH, '//div[@class="section-result"]')
            sleep(0.5)
            try:
                # added checking of network here to make sure there's internet before interacting
                self.wait_for_reconnection()
                results[curr_item].click()
            except Exception:
                # self.export_to_csv()
                self.wait_for_reconnection()  # added here to wait for reconnection before handling error
                wait.until(
                    exp_con.presence_of_element_located((
                        # FIXME: the problem is here, everytime there's a network problem, it goes down to this.
                        # TODO: i have resolved the issue by making wait_for_reconnection(). please check
                        By.XPATH, '//h1[contains(@class, "title-title")]'
                    ))
                )
            wait.until(
                exp_con.presence_of_element_located((
                    By.XPATH, '//h1[contains(@class, "title-title")]'
                ))
            )
            try:
                name = driver.find_element(By.XPATH, '//h1[contains(@class, "title-title")]').text
            except Exception:
                name = ''
            try:
                phone_number = driver.find_element(
                    By.XPATH,
                    '//span[@aria-label="Phone"]/following::span[@class="section-info-text"]'
                    '[1]/span[contains(@class,"-link")]'
                ).text
            except Exception:
                phone_number = ''
            try:
                address1 = driver.find_element(
                    By.XPATH,
                    '//span[@aria-label="Address"]/following::span[@class='
                    '"section-info-text"][1]/span[contains(@class,"-link")]'
                ).text
            except Exception:
                address1 = ''
            try:
                address2 = driver.find_element(
                    By.XPATH,
                    '//span[@aria-label="Address"]/following::span'
                    '[@class="section-info-text"][2]/span[contains(@class,"-link")]'
                ).text
            except Exception:
                address2 = ''
            try:
                website = driver.find_element(
                    By.XPATH,
                    '//*[@id="pane"]/div/div[1]/div/div/div[10]/div/div[1]/span[3]/span[3]'  # TODO: this is not a relative path. this should be fixed soon
                ).text
            except Exception:
                website = ''
            new_data = ((
                name, phone_number, address1, address2, website
            ))
            self.data.append(new_data)
            sleep(1)
            driver.back()
            # start of nested try-catch statements
            try:
                # added here to wait for reconnection before handling error
                self.wait_for_reconnection()
                wait.until(
                    exp_con.presence_of_element_located((
                        By.XPATH, '//div[@class="section-result"]'
                    ))
                )
            except selenium.common.exceptions.TimeoutException:
                try:
                    driver.back()
                    wait.until(
                        exp_con.presence_of_element_located((
                            By.XPATH, '//div[@class="section-result"]'
                        ))
                    )
                except selenium.common.exceptions.TimeoutException:
                    driver.back()
                    'Chromedriver might crash...'
                    self.export_to_csv()
            #

    def scrape(self, driver):
        has_next_page = True
        curr_page = 1
        # TODO: make initial checks here
        while has_next_page:
            self.scrape_results(driver, curr_page)
            sleep(1)
            curr_page += 1
            if curr_page == self.NO_PAGES+1:
                has_next_page = False
        self.export_to_csv()

    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.get_url(self.DRIVER_TITLE))
        sleep(2)
        self.scrape(driver)


if __name__ == '__main__':
    crawler = GoogleMapsCrawler('supermarkets in long island county, NY', 20, 20)
    crawler.main()
