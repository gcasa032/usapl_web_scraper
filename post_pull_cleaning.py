from re import U
from bs4 import BeautifulSoup
from requests import request, Session
import pandas as pd
import numpy as np
import util

data = pd.read_csv("data/usapl_data.csv", encoding='cp1252', low_memory=False, keep_default_na=False)

leng = len(data)

#TODO get unknown sex from previous meets

sesh = Session()

for x in data.index:
    if data.loc[x, 'equipment'] == 'Unknown' or data.loc[x, 'weight_class_kg'] == '':
        print('Processing: ', x, 'out of:', leng)
        lifter_id = str(data.loc[x, 'lifter_id'])
        instance_id = str(data.loc[x, 'instance_id'])

        res = util.scrape_lifter_view(sesh, lifter_id, instance_id)

        data.loc[x, 'equipment'] = res['equipment']
        data.loc[x, 'division'] = res['division']
        data.loc[x, 'weight_class_kg'] = res['weight_class']

        print(data.loc[x, 'equipment'], data.loc[x, 'division'], data.loc[x, 'weight_class_kg'])

data.to_csv('data/processed_usapl_data.csv', index = False)
