import csv
from genericpath import exists
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
from datetime import date

import config


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
    meet_date = meet_info[0].td.string.split()[0]
    if len(meet_info) >= 3:
        meet_state = meet_info[2].td.string
    else:
        meet_state = ""

    meet_results = meet.find('table', id='competition_view_results').find('tbody').find_all("tr")
    results_db = []

    for result in meet_results:
        cols = result.find_all("td")
        if len(cols) > 0:
            results_db.append(
                {
                    'date': meet_date,
                    'meet_state': meet_state,
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
