import datetime
import re
import requests
from bs4 import BeautifulSoup
from lxml import html


class VesselFinder:

    def __init__(self, imo=None):
        self.imo = imo
        self.url = None
        self.port = None
        self.expected = None
        self.headers = {
            'Content-Type': 'text/html;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/118.0.0.0 Safari/537.36'
        }

    def expected_arrivals(self, port="KWMEA001"):
        self.port = port
        self.url = f"https://www.vesselfinder.com/ports/{self.port}"
        response = requests.get(self.url, headers=self.headers)
        # Check if the request was successful
        if response.status_code == 200:
            excepted = []
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div with id 'tab-content'
            tab_content = soup.find('div', id='tab-content')

            if tab_content:
                # Find the table within the div
                table = tab_content.find('table')

                if table:
                    # Find the tbody within the table
                    tbody = table.find('tbody')

                    if tbody:
                        # Iterate through all table rows within the tbody
                        for row in tbody.find_all('tr'):
                            # Get the first 'td' element from the row
                            first_td = row.find('td')
                            if first_td:
                                try:
                                    date = datetime.datetime.strptime(first_td.get_text(), "%b %d, %H:%M").replace(
                                        year=datetime.datetime.today().year
                                    ) + datetime.timedelta(hours=3)
                                except:
                                    date = None
                                # Get the 'a' tag with class 'named-item'
                                named_item = row.find('a', class_='named-item')
                                imo_number = re.sub(r'(.+)/(\d+)', '\\2',
                                                    named_item.get('href')) if named_item else None

                                # Get the 'div' tag with class 'named-title'
                                named_title = row.find('div', class_='named-title')
                                title_text = named_title.get_text(strip=True) if named_title else None

                                # Get the 'div' tag with class 'named-subtitle'
                                named_subtitle = row.find('div', class_='named-subtitle')
                                subtitle_text = named_subtitle.get_text(strip=True) if named_subtitle else None

                                # Now you have the texts from the specific elements
                                excepted.append({
                                    'date': date,
                                    'imo': imo_number,
                                    'Vessel': title_text,
                                    'Type': subtitle_text
                                })
                    else:
                        print("No tbody found in the table.")
                        return None
                else:
                    print("No table found in the div.")
                    return None
            else:
                print("No div with id 'tab-content' found.")
                return None
        else:
            print(f"Failed to retrieve content, status code {response.status_code}")
            return None
        return excepted

    def particulars(self):
        self.url = f"https://www.vesselfinder.com/vessels/details/{self.imo}"
        xpath = "/html/body/div[1]/div/main/div/section[5]"
        response = requests.get(self.url, headers=self.headers)
        # Check if the request was successful
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            elements = tree.xpath(xpath)
            for element in elements:
                # Extract text or attributes from the element as needed
                text = element.text_content().strip()
                print(text)
                # IMO
                imo = re.search(r'IMO number(\d+)', text, re.IGNORECASE)
                imo = imo.group(1).strip() if imo else None
                # VESSEL NAME
                vessel = re.search(r'Vessel Name(.+)\b', text, re.IGNORECASE)
                vessel = vessel.group(1).strip() if vessel else None
                # Type
                type = re.search(r'Ship type(.+)\b', text, re.IGNORECASE)
                type = type.group(1).strip() if type else None
                # Flag
                flag = re.search(r'Flag(.+)\b', text, re.IGNORECASE)
                flag = flag.group(1).strip() if flag else None
                # Summer Deadweight (t)
                sdw = re.search(r'Summer Deadweight \(t\)(.+)\b', text, re.IGNORECASE)
                sdw = sdw.group(1).strip() if sdw else None
                # Length Overall (m)228
                length = re.search(r'Length Overall \(m\)(.+)\b', text, re.IGNORECASE)
                length = length.group(1).strip() if length else None
                # Year of Build2007
                year = re.search(r'Year of Build(\d+)', text, re.IGNORECASE)
                year = year.group(1).strip() if year else None

                vessel = {
                    'imo': imo,
                    'Vessel': vessel,
                    'Type': type,
                    'flag': flag,
                    'sdw': sdw,
                    'length': length,
                    'year': year,
                }
                return vessel
        else:
            print(f"Failed to retrieve content, status code {response.status_code}")
            return None
