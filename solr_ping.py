#!/usr/bin/env python

import sys
import requests
import json

# parse the solr status
"""
this does sadly not work on older versions of requests:
with requests.get(status_url) as get_data:
    solr_status = get_data.json()
"""
status_url = 'http://localhost:8983/solr/admin/cores?action=STATUS&wt=json'

# fetch status
try:
    get_data = requests.get(status_url, timeout=10)
    solr_status = get_data.json()
except requests.exceptions.RequestException as e:
    state = 2
    print('{} Solr_Ping - {}').format(state, e)
    sys.exit(2)

# fetch the solr cores
solr_core = []
for item in solr_status['status']:
    solr_core.append(item)

# run the check
try:
    for i in solr_core:
        url = 'http://localhost:8983/solr/{}/admin/ping'.format(i)
        data = requests.get(url)
        if 'OK' not in data.text:
            state = 2
            break
        else:
            state = 0
except requests.exceptions.RequestException as e:
    state = 2
    print('{} Solr_Ping - {}').format(state, e)
    sys.exit(2)

if state == 0:
    print('{} Solr_Ping - Core(s) is OK').format(state)
elif state == 2:
    print('{} Solr_Ping - Core: {} not responding OK').format(state, i)
