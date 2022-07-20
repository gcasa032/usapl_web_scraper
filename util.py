from __future__ import division
import csv
from genericpath import exists
from requests import request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
import cchardet as chardet
from datetime import date

import config

def update_division(curr_div, header):

    if curr_div is None:
        curr_div = {}

    if header is None:
            return curr_div

    header_text = header.get_text(strip=True)

    if header.get('class') and header['class'][0] == 'competition_view_event':
        curr_div['event'] = header_text
        return curr_div

    # Division Conditional
    curr_div['division'] = header_text.replace('Male', '').replace('Female', '').replace('MX', '').strip('- ')

    # Equipment Conditional

    if 'Raw with Wraps' in header_text:
        curr_div['equipment'] = 'Raw with Wraps'
    elif 'Raw' in header_text: 
        curr_div['equipment'] = 'Raw'
    elif curr_div['division'] in config.equipped_divisions: 
        curr_div['equipment'] = 'Equipped'
    else:
        curr_div['equipment'] = 'Unknown'

    # Sex Conditional

    if 'Male' in header_text:
        curr_div['sex'] = 'Male'
    elif 'Female' in header_text:
        curr_div['sex'] = 'Female'
    elif 'MX' in header_text:
        curr_div['sex'] = 'MX'
    else:
        curr_div['sex'] = 'Unknown'

    return curr_div


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
    division = {
        'event': '',
        'sex': '',
        'equipment': '',
        'division': ''
    }

    for result in meet_results:
        cols = result.find_all("td")

        division = update_division(division, result.find("th"))

        if len(cols) > 0:

            lifter_id = config.parse_lifter_id.findall(cols[2].a.get('href'))[0]
            instance_id = cols[8].get('id').split('_')[-1]

            results_db.append(
                {
                    'meet_id': id,
                    'lifter_id': lifter_id,
                    'instance_id': instance_id,
                    'date': meet_date,
                    'meet_name': meet_name,
                    'meet_state': meet_state,
                    'event': division["event"], 
                    'sex': division["sex"], 
                    'equipment': division["equipment"], 
                    'division': division["division"], 
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

# Will be used in post scrape processing
def scrape_lifter_view(lifter_id, instance_id):

    lifter_html = requests.get("https://usapl.liftingdatabase.com/lifters-view?id=" + str(lifter_id)).content

    lifter = BeautifulSoup(lifter_html, 'lxml').find('div', id='content').find('td', id= re.compile('^.*' + instance_id + '.*$')).parent

    meet_instance = lifter.find_all('td')

    # TODO Get unknown weight class
    abv_division = meet_instance[3].get_text(strip=True).split('-')
    weight_class = meet_instance[4].get_text(strip=True)

    if len(abv_division) > 1:
        equipment = config.division_map.get(abv_division[0])
        division = equipment + " " + config.division_map.get(abv_division[1]) 
    else:
        equipment = 'Equipped'
        division = config.division_map.get(abv_division[0])

    return {
        'division': division,
        'equipment': equipment,
        'weight_class': weight_class
    }


def parse_equipment(division):

    # Analyse all divisions found in database
    div_split = division.split('-')

    # Save 

    return

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
        
        
