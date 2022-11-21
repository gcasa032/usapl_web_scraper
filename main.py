import csv
from genericpath import exists
from datetime import date
from requests import request, Session
import config
import util

datastore_metadata = util.get_processed_ids()
all_meets = util.get_all_meets()
num_meets = len(all_meets)

# Check if datastores files exists
data_exists = True if exists(config.datastore['file']) else False
metadata_exists = True if exists(config.metastore['file']) else False

res_file = open(config.datastore['file'], "a")
metadata_file = open(config.metastore['file'], 'a')

res_writer = csv.DictWriter(res_file, config.datastore['header'], delimiter=',', lineterminator='\n')
meta_writer = csv.writer(metadata_file, delimiter=',', lineterminator='\n')

res_writer.writeheader() if not data_exists else None
meta_writer.writerow(config.metastore['header']) if not metadata_exists else None

sesh = Session()

for i, meet in enumerate(all_meets):

    if meet['id'] not in datastore_metadata:

        print("Processing meet: ", meet['id'], 'from ', meet['date'], '|| Progress: ', i+1, 'out of ', num_meets)

        meet_results = util.get_meet(sesh, meet['id'])

        res_writer.writerows(meet_results)
        meta_writer.writerow([meet['id'], meet['date'], date.today().strftime("%m/%d/%Y")])    

res_file.close()
metadata_file.close()

print("Data Pull Complete ")







