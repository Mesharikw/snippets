import re
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_except_arrivals():
    url = "https://www.marinetraffic.com/en/data/?asset_type=expected_arrivals&columns=shipname,recognized_next_port," \
          "reported_eta,arrived,show_on_live_map,dwt," \
          "ship_type&recognized_next_port_in|begins|MINA%20AL%20AHMADI|recognized_next_port_in=3191&arrival_time_gte" \
          "|gte|arrival_time_gte=0,43200&ship_type_in|in|Tankers|ship_type_in=8 "
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ag-grid-container")))
        element = driver.find_element_by_class_name('ag-grid-container').get_attribute('innerHTML')
        elements = driver.find_elements_by_class_name('ag-cell-content-link')
        i = 0
        links = []
        for element in elements:
            i += 1
            if i % 2 != 0:
                href = element.get_attribute('href')
                links.append(href)
        if links:
            for link in links:
                try:
                    driver.get(link)
                    time.sleep(5)
                    _ = driver.find_element_by_class_name('jss419')
                    vessel_type = _.get_attribute('title')
                    if str(vessel_type).title().strip() in ['Crude Oil Tanker']:
                        vessel = {
                            'vessel': _.find_element_by_xpath("..").text,
                            'imo': re.sub(r'(.+IMO:[^\d]+)', '',
                                          str(driver.find_element_by_class_name('jss424').text).strip()),
                            'eta': re.sub(r'ETA:', '', driver.find_element_by_xpath("""//*[
                        @id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[1]/div[3]/div/div[
                        2]/span/b""").find_element_by_xpath("..").text)
                        }
                        pprint(vessel)

                finally:
                    pass

    finally:
        pass
        driver.quit()


if __name__ == '__main__':
    get_except_arrivals()
