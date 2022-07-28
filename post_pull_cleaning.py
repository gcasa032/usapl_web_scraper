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

def clean():

    data = pd.read_csv('data/processed_usapl_data.csv', encoding='cp1252', low_memory=False, keep_default_na=False)
    data_index = list(data.index.values)

    threads = min(config.MAX_THREADS, len(data))

    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(clean_row, data, row): row for row in data_index}
        
        for fut in concurrent.futures.as_completed(futures):
            if fut.exception() is not None:
                failed_row = futures[fut]
                print(f'{failed_row} failed due to "{fut.exception()}" Retrying')
                executor.submit(clean_row, data, failed_row)
    t1 = time.time()

    data.to_csv('data/processed_usapl_data.csv', index = False, encoding='cp1252')
    # TODO get # of cleaned rows
    print(f"Data Pull Complete. It took {t1-t0} to clean {len(data)} rows")

def clean_row(data, index):

        # if data.loc[index, 'sex'] == 'Unknown':
        #     infer_sex(data.loc[index])

        if data.loc[index, 'equipment'] == 'Unknown' or data.loc[index, 'weight_class_kg'] == '':
        
            lifter_id = str(data.loc[index, 'lifter_id'])
            instance_id = str(data.loc[index, 'instance_id'])

            res = util.scrape_lifter_view(lifter_id, instance_id)

            data.loc[index, 'equipment'] = res['equipment']
            data.loc[index, 'division'] = res['division']
            data.loc[index, 'weight_class_kg'] = res['weight_class']

            print('Processed: ', lifter_id, index, '/', len(data))


# def infer_sex(row):

#     # will weight class always be there?
#         # maybe run cleaning first. analyze the output
#         # weight class is more likely to be there after cleaning runs
    
#     # if we cant infer with weight class we have to look at past meets so we have to look at data.


#     print(row)



clean()