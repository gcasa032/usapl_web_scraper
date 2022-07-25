import csv
from genericpath import exists
from datetime import date
import time
from requests import request, Session
import config
import util
import concurrent.futures

datastore_metadata = util.get_processed_ids()
all_meets = util.get_all_meets()[0:300]
num_meets = len(all_meets)

# Check if datastores files exists
data_exists = True if exists(config.datastore['file']) else False
metadata_exists = True if exists(config.metastore['file']) else False

res_file = open(config.datastore['file'], "a+")
res_writer = csv.DictWriter(res_file, config.datastore['header'], delimiter=',', lineterminator='\n')

metadata_file = open(config.metastore['file'], 'a+')
meta_writer = csv.writer(metadata_file, delimiter=',', lineterminator='\n')

res_writer.writeheader() if not data_exists else None
meta_writer.writerow(config.metastore['header']) if not metadata_exists else None

def scrape_meet(meet):

    if meet['id'] not in datastore_metadata:

        meet_results = util.get_meet(meet['id'])

        res_writer.writerows(meet_results)
        meta_writer.writerow([meet['id'], meet['date'], date.today().strftime("%m/%d/%Y")])    

        print("Successfully processed meet: ", meet['id'], 'from ', meet['date']) 

threads = min(config.MAX_THREADS, num_meets) 

t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    futures = {executor.submit(scrape_meet, meet): meet for meet in all_meets}

    for fut in concurrent.futures.as_completed(futures):
            if fut.exception() is not None:
                data = futures[fut]
                print(data["id"], 'failed due to', fut.exception(), 'Retrying')
                executor.submit(scrape_meet, data)
t1 = time.time()

res_file.close()
metadata_file.close()

print(f"Data Pull Complete. It took {t1-t0} to scrape {num_meets} meets")

# print("Starting post data pull cleaning")
# post_pull_cleaning.clean()









