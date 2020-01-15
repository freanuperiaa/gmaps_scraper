import sys
from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as exp_con
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.ui as ui
import pandas as pd

# from exceptions import *


class GoogleMapsCrawler:
    NO_RESULTS = 20
    DRIVER_TITLE = 'nail salons in south queens new york'
    data = []

    def get_waiter(self, driver, timeout=10):
        return ui.WebDriverWait(driver, timeout)

    def export_to_csv(self, data_frame):
        print('the data frame contains', len(data_frame), 'rows.')
        file_name = input('enter file name for csv')
        data_frame.to_csv(file_name)

    def scrape_results(self, driver, curr_page):
        wait = self.get_waiter(driver)  # init waiter for this method

        # i had to do this because google chrome seems to have a weird behaviour
        for x in range(self.NO_RESULTS):
            sys.stdout.write('{}th iteration\r'.format(x))
            sys.stdout.flush()
            for x in range((curr_page-1)):
                print('went to next page')
                next_button = driver.find_element(By.XPATH, '//div/button[contains(@aria-label,"Next page")]')
                if next_button.is_enabled():
                    next_button.click()
                try:
                    sleep(5)
                    wait.until(
                        exp_con.presence_of_element_located((
                            By.XPATH, '//div[@class="section-result"]'
                        ))
                    )
                except Exception:
                    try:
                        sleep(5)
                        wait.until(
                            exp_con.presence_of_element_located((
                                By.XPATH, '//div[@class="section-result"]'
                            ))
                        )
                    except Exception:
                        pass
            results = driver.find_elements(By.XPATH, '//div[@class="section-result"]')
            results[x].click()
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
            print(name, ' ', phone_number, ' ', address1, ' ', address2)
            driver.execute_script("window.history.go(-1)")
            # start of nested try-catch statements
            try:
                wait.until(
                    exp_con.presence_of_element_located((
                        By.XPATH, '//div[@class="section-result"]'
                    ))
                )
            except selenium.common.exceptions.TimeoutException:
                try:
                    driver.execute_script("window.history.go(-1)")
                    wait.until(
                        exp_con.presence_of_element_located((
                            By.XPATH, '//div[@class="section-result"]'
                        ))
                    )
                except selenium.common.exceptions.TimeoutException:
                    driver.execute_script("window.history.go(-1)")
            #
            wait.until(
                exp_con.presence_of_element_located((
                    By.XPATH, '//div[@class="section-result"]'
                ))
            )
            sleep(1)

    def scrape(self, driver):
        has_next_page = True
        curr_page = 1
        # TODO: make initial checks here
        while has_next_page:
            self.scrape_results(driver, curr_page)
            sleep(3)
            curr_page += 1
        # self.scrape_results(driver)
        # # TODO: go to next page
        # next_button = driver.find_element(By.XPATH, '//div/button[contains(@aria-label,"Next page")]')
        # next_button.click()
        # sleep(5)
        # if next_button.is_enabled():
        #     next_button.click()

    def main(self):
        driver = webdriver.Chrome()
        driver.get('https://www.google.com/maps/search/nail+salons+in+south+queens+new+york')
        sleep(2)
        self.scrape(driver)


if __name__ == '__main__':
    crawler = GoogleMapsCrawler()
    crawler.main()
