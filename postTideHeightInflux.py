# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:51:32 2018

@author: phutchinson
"""

import requests
import json
import datetime
import time 
import sys

from influxdb import InfluxDBClient


# Function to return sea height from Environment Agency Tide Gauge API
def getSeaHeight(time):
    # API source data is slow to update so subtract 2hrs from now
    nowTime = time - datetime.timedelta(hours=2)
    # Round measurement to floor 15 minutes (Sample T of Tide Times)
    #nowTime += datetime.timedelta(minutes=15)
    nowTime -= datetime.timedelta(minutes=nowTime.minute % 15)
    nowTimeFormatMetApi = nowTime.strftime("%Y-%m-%dT%H-%M-00Z")

    response = requests.get(
        "http://environment.data.gov.uk/flood-monitoring/data/readings/E72539-level-tidal_level-Mean-15_min-mAOD/{0}".
        format(nowTimeFormatMetApi))

    # Parse JSON reponse for sea height (Meters)
    if response.status_code == 200:
        parsed_json = json.loads(response.content.decode('utf-8'))
        return parsed_json['items']['value'], parsed_json['items']['dateTime']
    else:
        #print("Err. no data available")
        return "Err. no data available"

client = InfluxDBClient(host="HOST",port=8086, username="USR",password="PWD")

client.switch_database('telegraf')



while True:
    try:

        seaHeight, sampleDateTime = getSeaHeight(datetime.datetime.now())

        json_body = [
                {
                    "measurement": "seaHeightBeta",
                    "tags": {
                    },
                    "time": sampleDateTime,
                    "fields": {
                        "seaHeight": seaHeight
                        }
                        }
                        ]
        
        client.write_points(json_body)
        print(seaHeight)
        print(sampleDateTime)
        
    except: 
        print("Err. Exception unpacking message @ ", datetime.datetime.now(), sys.exc_info()[0])
    time.sleep(900)
