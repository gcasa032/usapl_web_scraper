import pandas as pd
import config
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

data = pd.read_csv(config.datastore['file'], encoding='cp1252', low_memory=False, keep_default_na=False)
clean_data = pd.read_csv('data/processed_usapl_data.csv', encoding='cp1252', low_memory=False, keep_default_na=False)

data_index = list(data.index.values)

q_num_rows_to_clean = lambda df :f"""
SELECT count(*) as count
FROM
    (
        SELECT lifter_id
        FROM {df}
        WHERE equipment = 'Unknown' OR weight_class_kg = ''
    )
"""

print('Raw data: ', pysqldf(q_num_rows_to_clean('data')).loc[0, 'count'])
print('Cleaned data: ', pysqldf(q_num_rows_to_clean('clean_data')).loc[0, 'count'])

# num_rows = 0

# for index in data_index:
#     if data.loc[index, 'equipment'] == 'Unknown' or data.loc[index, 'weight_class_kg'] == '':
#         num_rows += 1

# print(num_rows)