import sys
from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as exp_con
import pandas as pd
#
# from exceptions import *
from selenium.webdriver.support.wait import WebDriverWait


def export_to_csv(data_frame):
    print('the data frame contains', len(data_frame), 'rows.')
    file_name = input('enter file name for csv: ')
    data_frame.to_csv(file_name)


def scrape_from_page(driver):
    # check table where data is contained
    table_result = driver.find_elements(By.XPATH, '//table[@id="deals_filter_result"]/tbody/tr')
    # if table_result in [[], 0, None]:
    #     raise ElementNotFoundException
    page_data = []  # variable to contain all rows in the page
    curr_iteration = 0
    for row in table_result:
        curr_iteration += 1
        try:
            address = row.find_element_by_class_name('deals1').text
        except Exception:
            address = ''
        try:
            deals2 = row.find_element_by_class_name('deals2').text
        except Exception:
            deals2 = ''
        try:
            tenant = row.find_element_by_class_name('deals3').text
        except Exception:
            tenant = ''
        try:
            landlord = row.find_element_by_class_name('deals4').text
        except Exception:
            landlord = ''
        try:
            borough = row.find_element_by_class_name('deals5').text
        except Exception:
            borough = ''
        try:
            size = row.find_element_by_class_name('deals6').text
        except Exception:
            size = ''
        try:
            deals7 = row.find_element_by_class_name('deals7').text
        except Exception:
            deals7 = ''
        try:
            deals8 = row.find_element_by_class_name('deals8').text
        except Exception:
            deals8 = ''
        try:
            neighborhood = row.find_element_by_class_name('deals9').text
        except Exception:
            neighborhood = ''
        try:
            event_date = row.find_element_by_class_name('deals10').text
        except Exception:
            event_date = ''
        try:
            tenant_rep_agent = row.find_element_by_class_name('deals11').text
        except Exception:
            tenant_rep_agent = ''
        try:
            landlord_rep_agent = row.find_element_by_class_name('deals12').text
        except Exception:
            landlord_rep_agent = ''
        try:
            event = row.find_element_by_class_name('deals13').text
        except Exception:
            event = ''
        try:
            publication_date = row.find_element_by_class_name('deals14').text
        except Exception:
            publication_date = ''
        try:
            tenant_rep_firm = row.find_element_by_class_name('deals15').text
        except Exception:
            tenant_rep_firm = ''
        try:
            landlord_rep_firm = row.find_element_by_class_name('deals16').text
        except Exception:
            landlord_rep_firm = ''
        new_row = ((
            address, deals2, tenant, landlord, borough, size, deals7, deals8,
            neighborhood, event_date, tenant_rep_agent, landlord_rep_agent,
            event, publication_date, tenant_rep_firm, landlord_rep_firm
        ))
        sys.stdout.write("\r%d%%" % curr_iteration)
        sys.stdout.flush()
        page_data.append(new_row)
    return page_data


def scrape(driver):
    trd_data = []
    # check if we're on the current page
    curr_page = int(driver.find_element(By.XPATH, '//div[@class="deals_pagination_pages"]/span[@class="red"]').text)
    # iterate through every page of the results
    while curr_page <= 144:
        print('current page:', curr_page)
        print('no. of data scraped:', len(trd_data))
        curr_page_data = scrape_from_page(driver)
        for row_data in curr_page_data:
            trd_data.append(row_data)
        # next_page = driver.find_element(
        #     By.XPATH, '//div[@class="deals_pagination_pages"]/span[@class="red"]//following::a[1]'
        # )
        next_page = WebDriverWait(driver, 15).until(
            exp_con.presence_of_element_located((
                By.XPATH, '//div[@class="deals_pagination_pages"]/span[@class="red"]//following::a[1]'
            ))
        )
        next_page.click()
        curr_page += 1
        sleep(2)

    data_frame = pd.DataFrame(trd_data, columns=[
        'Address', 'deals2', 'Tenant', 'Landlord', 'Borough', 'Size',
        'deals7', 'deals8', 'Neighborhood', 'Event Date', 'Tenant Rep. Agent',
        'Landlord Rep. Agent', 'Event', 'Publication Date', 'Tenant Rep. Firm',
        'Landlord Rep. Firm'
    ])
    export_to_csv(data_frame)


def ready_scrape(driver):
    print('reached here')
    # retail_listing_checkbox = driver.find_element(By.XPATH, '//input[@name="retail_leasing"]')
    # manhattan_checkbox = driver.find_element(By.XPATH, '//input[@name="manhattan"]')
    # bronx_checkbox = driver.find_element(By.XPATH, '//input[@name="bronx"]')
    # brooklyn_checkbox = driver.find_element(By.XPATH, '//input[@name="brooklyn"]')
    # queens_checkbox = driver.find_element(By.XPATH, '//input[@name="queens"]')
    # staten_island_checkbox = driver.find_element(By.XPATH, '//input[@name="statend_island"]')
    # submit_button = driver.find_element(By.XPATH, '//input[@name="deal_page_filter"]')
    # # click buttons that will show all listings in all boroughs
    # retail_listing_checkbox.click()
    # manhattan_checkbox.click()
    # bronx_checkbox.click()
    # brooklyn_checkbox.click()
    # queens_checkbox.click()
    # staten_island_checkbox.click()
    # submit_button.click()
    sleep(2)
    scrape(driver)


def main():
    driver = webdriver.Chrome()
    driver.get('https://therealdeal.com/new-research/dealsheets/')
    ready_scrape(driver)


if __name__ == '__main__':
    main()
