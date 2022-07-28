import re

MAX_THREADS = 10

metastore = dict(
    file = 'data/multithread/meet_metadata.csv',
    header = [
        'id',
        'date',
        'processing_date'
        ]
    )

datastore = dict(
    file = 'data/multithread/usapl_data.csv',
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
    "Youth 1",
    "Youth 2",
    "Youth 3",
    "LW",
    "HW"]
)

parse_lifter_id = re.compile(r'^lifters-view\?id=(\d+)')

division_map = {
    'R': 'Raw',
    'RW' : 'Raw with Wraps',
    'AA': 'Adaptive Athletes',
    'PRO': 'Open Pro',
    'SO': 'Special Olympian',
    'GL': 'Guest Lifter',
    'O': 'Open',
    'JR': 'Junior',
    'T1': 'Teen 1',
    'T2': 'Teen 2',
    'T3': 'Teen 3',
    'Y1': 'Youth 1',
    'Y2': 'Youth 2',
    'Y3': 'Youth 3',
    'M': 'Master',
    'M1': 'Master 1',
    'M1A': 'Master 1a',
    'M1B': 'Master 1a',
    'M2': 'Master 2',
    'M2A': 'Master 2a',
    'M2B': 'Master 2b',
    'M3': 'Master 3',
    'M3A': 'Master 3a',
    'M3B': 'Master 3b',
    'M4': 'Master 4',
    'M4A': 'Master 4a',
    'M4B': 'Master 4b',
    'M5': 'Master 5',
    'M5A': 'Master 5a',
    'M5B': 'Master 5b',
    'PF': 'Police and Fire',
    'HS': 'High School',
    'C': 'Collegiate',
    'G': 'Military Open'
}

