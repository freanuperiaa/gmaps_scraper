from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
#
# from exceptions import *


def export_to_csv(data_frame):
    print('the data frame contains', len(data_frame), 'rows.')
    file_name = input('enter file name for csv')
    data_frame.to_csv(file_name)


def scrape(driver):
    # check table where data is contained
    table_result = driver.find_elements(By.XPATH, '//table[@id="deals_filter_result"]/tbody/tr')
    # if table_result in [[], 0, None]:
    #     raise ElementNotFoundException
    page_data = []  # variable to contain all rows
    for row in table_result:
        address = row.find_element_by_class_name('deals1').text
        deals2 = row.find_element_by_class_name('deals2').text
        tenant = row.find_element_by_class_name('deals3').text
        landlord = row.find_element_by_class_name('deals4').text
        borough = row.find_element_by_class_name('deals5').text
        size = row.find_element_by_class_name('deals6').text
        deals7 = row.find_element_by_class_name('deals7').text
        deals8 = row.find_element_by_class_name('deals8').text
        neighborhood = row.find_element_by_class_name('deals9').text
        event_date = row.find_element_by_class_name('deals10').text
        tenant_rep_agent = row.find_element_by_class_name('deals11').text
        landlord_rep_agent = row.find_element_by_class_name('deals12').text
        event = row.find_element_by_class_name('deals13').text
        publication_date = row.find_element_by_class_name('deals14').text
        tenant_rep_firm = row.find_element_by_class_name('deals15').text
        landlord_rep_firm = row.find_element_by_class_name('deals16').text
        new_row = ((
            address, deals2, tenant, landlord, borough, size, deals7, deals8,
            neighborhood, event_date, tenant_rep_agent, landlord_rep_agent,
            event, publication_date, tenant_rep_firm, landlord_rep_firm
       ))
        print('processing_  ')
        page_data.append(new_row)
        # put the data in page_data to a data_frame
    data_frame = pd.DataFrame(page_data, columns=[
        'Address', 'deals2', 'Tenant', 'Landlord', 'Borough', 'Size',
        'deals7', 'deals8', 'Neighborhood', 'Event Date', 'Tenant Rep. Agent',
        'Landlord Rep. Agent', 'Event', 'Publication Date', 'Tenant Rep. Firm',
        'Landlord Rep. Firm'
    ])
    export_to_csv(data_frame)


def ready_scrape(driver):
    print('reached here')
    retail_listing_checkbox = driver.find_element(By.XPATH, '//input[@name="retail_leasing"]')
    manhattan_checkbox = driver.find_element(By.XPATH, '//input[@name="manhattan"]')
    bronx_checkbox = driver.find_element(By.XPATH, '//input[@name="bronx"]')
    brooklyn_checkbox = driver.find_element(By.XPATH, '//input[@name="brooklyn"]')
    queens_checkbox = driver.find_element(By.XPATH, '//input[@name="queens"]')
    staten_island_checkbox = driver.find_element(By.XPATH, '//input[@name="statend_island"]')
    submit_button = driver.find_element(By.XPATH, '//input[@name="deal_page_filter"]')
    # click buttons that will show all listings in all boroughs
    retail_listing_checkbox.click()
    manhattan_checkbox.click()
    bronx_checkbox.click()
    brooklyn_checkbox.click()
    queens_checkbox.click()
    staten_island_checkbox.click()
    submit_button.click()
    sleep(3)
    scrape(driver)


def main():
    driver = webdriver.Chrome()
    driver.get('https://therealdeal.com/new-research/dealsheets/')
    ready_scrape(driver)


if __name__ == '__main__':
    main()
