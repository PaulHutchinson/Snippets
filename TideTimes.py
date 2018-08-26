# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 17:14:13 2018
Python script to extract sea hights from location E72539
@author: phutchinson
"""

import requests
import json
import datetime
import time


# Function to return sea height from Environment Agency Tide Gauge API
def getSeaHeight(time):
	# API source data is slow to update so subtract 2hrs from now
	nowTime = time - datetime.timedelta(hours=2)
	# Round measurement to floor 15 minutes (Sample T of Tide Times)
	#nowTime += datetime.timedelta(minutes=15)
	nowTime -= datetime.timedelta(minutes=nowTime.minute % 15)
	nowTimeFormatMetApi = nowTime.strftime("%Y-%m-%dT%H-%M-00Z")
	#print(nowTimeFormatMetApi)

	response = requests.get(
		"http://environment.data.gov.uk/flood-monitoring/data/readings/E72539-level-tidal_level-Mean-15_min-mAOD/{0}".
		format(nowTimeFormatMetApi))

	# Parse JSON reponse for sea height (Meters)
	if response.status_code == 200:
		parsed_json = json.loads(response.content.decode('utf-8'))
		#print(parsed_json['items']['dateTime'])
		#print(parsed_json['items']['value'])
		return parsed_json['items']['value'], parsed_json['items']['dateTime']
	else:
		#print("Err. no data available")
		return "Err. no data available"


while (True):
    try:
        seaHeight, sampleDateTime = getSeaHeight(datetime.datetime.now())
        print(seaHeight)
        print(sampleDateTime)
    except: 
        print("Err. Exception unpacking message @ ", datetime.datetime.now(), sys.exc_info()[0])
        #raise
    time.sleep(900)
