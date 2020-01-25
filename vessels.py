import re

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_vessel(imo):
    url = f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo," \
          f"recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map," \
          f"time_of_latest_position,lat_of_latest_position,lon_of_latest_position&quicksearch|begins|quicksearch={imo} "
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    vessel = False
    try:
        xpath = """//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[1]/div/div/div[3]/div/div/a"""
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        href = driver.find_element_by_xpath(xpath).get_attribute('href')
        driver.get(href)
        element_ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'imo')))
        vessel = {
            'imo': re.sub(r'^.+:\s', '', driver.find_element_by_id('imo').text),
            'name': re.sub(r'^.+:\s', '', driver.find_element_by_id('shipName').text),
            'type': re.sub(r'^.+:\s', '', driver.find_element_by_id('shipTypeSpecific').text),
            'mmsi': re.sub(r'^.+:\s', '', driver.find_element_by_id('mmsi').text),
            'callSign': re.sub(r'^.+:\s', '', driver.find_element_by_id('callSign').text),
            'flag': re.sub(r'^.+:\s', '', driver.find_element_by_id('flag').text),
            'summerDwt': re.sub(r'^.+:\s', '', driver.find_element_by_id('summerDwt').text)[:-1],
            'lengthOverallBreadthExtreme': re.sub(r'^.+:\s', '',
                                                  driver.find_element_by_id('lengthOverallBreadthExtreme').text),
            'yearBuild': re.sub(r'^.+:\s', '', driver.find_element_by_id('yearBuild').text),
        }
    finally:
        driver.quit()
    return vessel

