import re


metastore = dict(
    file = 'data/meet_metadata.csv',
    header = [
        'id',
        'date',
        'processing_date'
        ]
    )

datastore = dict(
    file = 'data/usapl_data.csv',
    header = [
        'date',
        'meet_id',
        'meet_name',
        'meet_state',
        'event',
        'sex',
        'equipment',
        'division',
        'weight_class_kg', 
        'placing', 
        'name', 
        'lifter_yob', 
        'team', 
        'lifter_state', 
        'lot_number', 
        'lifter_weight', 
        'squat1',
        'squat2',
        'squat3',
        'bench1', 
        'bench2',
        'bench3',  
        'deadlift1', 
        'deadlift2',
        'deadlift3',
        'total', 
        'dots', 
        'drug_test'
        ]
    )

parse_lifter_id = re.compile(r'^lifters-view\?id=(\d+)')

parse_lifter_instance_id = re.compile(r'^lifters-view\?id=(\d+)')

