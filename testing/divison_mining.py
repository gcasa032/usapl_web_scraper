from bs4 import BeautifulSoup
import pandas as pd
import requests


data = pd.read_csv("data/usapl_data.csv", encoding='cp1252', low_memory=False)


# Bug where no division is specified only Male or Female
no_div = data[data["division"].isnull()]

# All affected meets in numpy.ndarray
affected_meets = no_div.meet_id.unique()

# for each meet get if raw or equipped
for meet in affected_meets:

    url = "https://usapl.liftingdatabase.com/competitions-view?id=" + str(meet)
    print(url)

    html_req = requests.get(url)
    html = html_req.content

    print(html_req.status_code)

    meet_res = BeautifulSoup(html, 'lxml').find('div', id='content')
    meet_res = meet_res.find('table', id='competition_view_results')

    if meet_res is not None:
        meet_res_table = meet_res.find('tbody').find_all("th")

        for res in meet_res_table:
            if res.get('class'):
                meet_res_table.remove(res)

        print(meet_res_table)

    else:
        continue

    print(meet, len(meet_res_table))