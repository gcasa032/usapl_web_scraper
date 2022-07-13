import util
import csv
from genericpath import exists
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
from datetime import date

import config


util.get_lifter_meet_instance('120298', '226425')

# util.get_meet('119751')

# test = 'lift_120298_1_1_226424'

# test = test.split('_')[-1]

