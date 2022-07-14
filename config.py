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
        'meet_id',
        'lifter_id',
        'instance_id',
        'date',
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

equipped_divisions = set(
    ["Collegiate",
    "Guest Lifter",
    "Heavyweight",
    "High School",
    "High School JV",
    "High School Varsity",
    "Junior",
    "Lightweight",
    "Master",
    "Master 1",
    "Master 1a",
    "Master 1b",
    "Master 2",
    "Master 2a",
    "Master 2b",
    "Master 3",
    "Master 3a",
    "Master 3b",
    "Master 4",
    "Master 4a",
    "Master 4b",
    "Master 5",
    "Master 5a",
    "Military Open",
    "Open",
    "Special Olympian",
    "Sub Junior",
    "Teen",
    "Teen 1",
    "Teen 2",
    "Teen 3",
    "Youth",
    "Youth 2",
    "Youth 3",
    "LW",
    "HW"]
)

parse_lifter_id = re.compile(r'^lifters-view\?id=(\d+)')

