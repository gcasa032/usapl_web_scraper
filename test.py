from bs4 import BeautifulSoup
import requests
import util

def get_row_headers(id):

    meet_html = requests.get("https://usapl.liftingdatabase.com/competitions-view?id=" + str(id)).content

    meet = BeautifulSoup(meet_html, 'lxml').find('div', id='content')

    meet_results_table = meet.find('table', id='competition_view_results')

    if meet_results_table is not None:
        meet_results = meet_results_table.find('tbody').find_all("tr")
    else:
        return []

    results_db = []

    for result in meet_results:
        cols = result.find("th")
        if cols is not None and cols.get('class') is None:
            results_db.append(cols.get_text(strip=True))

    return results_db

meets = util.get_all_meets()[1:40]

all_headers = set()

for meet in meets:
    print('processing ', meet['id'])
    hed_list = get_row_headers(meet['id'])
    all_headers.update(hed_list)


for header in all_headers:
    
    header = header.replace('Male', '')
    header = header.replace('Female', '')
    header = header.strip('- ')

    print(header)
