from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from tinydb import TinyDB, Query


def check_moi(civil_id, **kwargs):

    url = f"https://portal.acs.moi.gov.kw/wps/portal/violations?systemSelection=1&numberType=1&numberValue={civil_id}" \
          f"&carNumberGoverCode=&licneseType=3&purpose=0&violYear=0&violGover=0&secondPartOfnewcarno=0" \
          f"&embassyTextField=0&QuickAccess='GO' "
    db = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{civil_id}.json'))
    ft = Query()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    fines = list()
    new = list()
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "myStyle11")))
        elements = driver.find_elements_by_class_name("myStyle11")
        for element in elements:
            html = element.get_attribute('innerHTML')
            fine = dict()
            soup = BeautifulSoup(html, "html.parser")
            tables = soup.findAll('table')[4:]

            table1 = tables[0].find('tbody')
            trs_table1 = table1.findAll('tr')
            table2 = tables[1].find('tbody')
            trs_table2 = table2.findAll('tr')[1]

            fine['daftar'] = trs_table1[0].findAll('td')[0].text.strip()
            fine['type'] = trs_table1[1].findAll('td')[0].text.strip()
            fine['timestamp'] = trs_table1[3].findAll('td')[0].text.strip()
            fine['speed'] = trs_table1[4].findAll('td')[0].text.strip()
            fine['location'] = trs_table1[5].findAll('td')[0].text.strip()
            fine['points'] = trs_table2.findAll('td')[0].text.strip()
            fine['fine'] = trs_table2.findAll('td')[1].text.strip()
            fine['reason'] = trs_table2.findAll('td')[5].text.strip()
            fine['evidence'] = trs_table2.findAll('td')[6].text.strip()
            fine['action'] = trs_table2.findAll('td')[7].text.strip()
            fines.append(fine)
            db_ = db.search(ft.daftar == fine['daftar'])

            if db_ == list():
                daftar = fine['daftar']
                print(f'* new fine has been raised to db. #{daftar}')
                db.insert(fine)
                new.append(fine)
    finally:
        driver.quit()
        if len(db.all()) != len(fines):
            db.purge()
            for fine in fines:
                db.insert(fine)
        total = sum(list(map(lambda a: float(a.get('fine')), db.all())))
