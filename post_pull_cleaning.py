from re import U
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import util

data = pd.read_csv("data/usapl_data.csv", encoding='cp1252', low_memory=False)

num = 0

for x in data.index:
    if data.loc[x, 'equipment'] == 'Unknown':
        lifter_id = str(data.loc[x, 'lifter_id'])
        instance_id = str(data.loc[x, 'instance_id'])

        res = util.scrape_lifter_view(lifter_id, instance_id)

        data.loc[x, 'equipment'] = res['equipment']
        data.loc[x, 'division'] = res['division']

        print(data.loc[x, 'equipment'], data.loc[x, 'division'])
