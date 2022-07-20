from re import U
import time
from bs4 import BeautifulSoup
from requests import request, Session
import pandas as pd
import numpy as np
import util
import config
import concurrent.futures

#TODO get unknown sex from previous meets


data = pd.read_csv(config.datastore['file'], encoding='cp1252', low_memory=False, keep_default_na=False)
data_index = list(data.index.values)
leng = len(data)
print(leng)

def clean_row(index):


    if data.loc[index, 'equipment'] == 'Unknown' or data.loc[index, 'weight_class_kg'] == '':
        print('Processing: ', index, 'out of:', leng)
        lifter_id = str(data.loc[index, 'lifter_id'])
        instance_id = str(data.loc[index, 'instance_id'])

        res = util.scrape_lifter_view(lifter_id, instance_id)
        print(res)

        data.loc[index, 'equipment'] = res['equipment']
        data.loc[index, 'division'] = res['division']
        data.loc[index, 'weight_class_kg'] = res['weight_class']

        print(data.loc[index, 'equipment'], data.loc[index, 'division'], data.loc[index, 'weight_class_kg'])


def clean():

    threads = min(config.MAX_THREADS, len(data))

    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(clean_row, data_index)
    t1 = time.time()

    data.to_csv('data/processed_usapl_data.csv', index = False)

clean()