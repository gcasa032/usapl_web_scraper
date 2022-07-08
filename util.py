from __future__ import division
import csv
from genericpath import exists
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
from datetime import date

import config

# Gets all lifters from USAPL Database and returns a set of lifter IDs
def get_all_lifters():
    
    page = 1
    url = 'https://usapl.liftingdatabase.com/lifters-default?p='
    lifters_db = set()

    parse_id = re.compile(r'^lifters-view\?id=(\d+)')

    while (True) :
        lifters_html = requests.get(url+str(page)).content
        lifters = BeautifulSoup(lifters_html, 'lxml').find('table', class_ = 'tabledata').find("tbody").find_all("tr")

        if len(lifters) == 0:
            break
        else:
            for lifter in lifters:
                lifters_db.add(parse_id.findall(lifter.find("td").a['href'])[0])
            page += 1

    return lifters_db


# Gets all meets from USAPL Database and retures as a List of dictionaries
def get_all_meets():


    meets_html = requests.get("https://usapl.liftingdatabase.com/competitions").content
    meets = BeautifulSoup(meets_html, 'lxml').find('table', class_ = 'tabledata').find("tbody").find_all("tr")

    parse_id = re.compile(r'^competitions-view\?id=(\d+)')
    meet_db = []

    for meet in meets:
        cols = meet.find_all("td")
        meet_db.append(
            {
                'date': cols[0].string,
                'id': parse_id.findall(cols[1].a['href'])[0]
            }
        )

    return meet_db

# Given a meet ID. This function will return all records from that meet as a list of dictionaries.
def get_meet(id):


    meet_html = requests.get("https://usapl.liftingdatabase.com/competitions-view?id=" + str(id)).content

    meet = BeautifulSoup(meet_html, 'lxml').find('div', id='content')

    meet_info = meet.find('table').tbody.find_all('tr')
    meet_name = meet.find('h3').string
    meet_date = meet_info[0].td.string.split()[0]
    if len(meet_info) >= 3:
        meet_state = meet_info[2].td.string
    else:
        meet_state = ""

    meet_results_table = meet.find('table', id='competition_view_results')

    if meet_results_table is not None:
        meet_results = meet_results_table.find('tbody').find_all("tr")
    else:
        return []

    results_db = []
    division = Division()

    for result in meet_results:
        cols = result.find_all("td")

        division.update(result.find("th"))

        if len(cols) > 0:
            results_db.append(
                {
                    'date': meet_date,
                    'meet_id': id,
                    'meet_name': meet_name,
                    'meet_state': meet_state,
                    'event': division.event, # Powerlifting, Bench, Deadlift, Push Pull, ...
                    'sex': division.sex, # Male, female
                    'equipment': division.equipment, # Equipped, Raw, Raw with Wraps...
                    'division': division.division, # Junior, Open, Master I,....
                    'weight_class_kg': cols[0].string,
                    'placing': cols[1].string,
                    'name': cols[2].string,
                    'lifter_yob': cols[3].string,
                    'team': cols[4].a.string,
                    'lifter_state': cols[5].string,
                    'lot_number': cols[6].string,
                    'lifter_weight': cols[7].string,
                    'squat1' : cols[8].get_text(strip=True),
                    'squat2' : cols[9].get_text(strip=True),
                    'squat3' : cols[10].get_text(strip=True),
                    'bench1' : cols[11].get_text(strip=True),
                    'bench2' : cols[12].get_text(strip=True),
                    'bench3' : cols[13].get_text(strip=True),
                    'deadlift1' : cols[14].get_text(strip=True),
                    'deadlift2' : cols[15].get_text(strip=True),
                    'deadlift3' : cols[16].get_text(strip=True),
                    'total': cols[17].get_text(strip=True),
                    'dots': cols[18].get_text(strip=True),
                    'drug_test': cols[20].get_text(strip=True)
                }
            )

    return results_db

# Access metadata and return set of processed IDs
def get_processed_ids():
    
    metastore = config.metastore['file']
    processed_meets = set()

    if not exists(metastore):
        return processed_meets

    data = open(metastore)
    reader = csv.reader(data)
    header = next(reader)

    for row in reader:
        processed_meets.add(row[0])

    data.close()

    return processed_meets


class Division:

    def __init__(self) -> None:
        self.event = ''
        self.sex = ''
        self.equipment = ''
        self.division = ''

    def update(self, header):
        
        if header is None:
            return

        header_text = header.get_text(strip=True)

        if header.get('class') and header['class'][0] == 'competition_view_event':
            self.event = header_text
            return

        self.meet_division = header_text

        # Equipment Conditional

        if 'Raw with Wraps' in header_text:
            self.equipment = 'Raw with Wraps'
        elif 'Raw' in header_text:
            self.equipment = 'Raw'
        else:
            self.equipment = 'Equipped'

        # Sex Conditional

        if 'Male' in header_text:
            self.sex = 'Male'
        elif 'Female' in header_text:
            self.sex = 'Female'

        # Division Conditional
        self.division = header_text.replace('Male', '').replace('Female', '').strip('- ')

        return
        
        
