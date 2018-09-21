"""
Created on Fri Sep 21 12:40:48 2018

@author: phutchinson
"""
import paho.mqtt.client as mqtt
import json

import numpy as np
from numpy import genfromtxt
X = genfromtxt('data.csv', delimiter=',')
Y = genfromtxt('class.csv', delimiter=',')

pcaStatePredict = {'pcaStatePredict': 1}

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(X, Y)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("v1/devices/me/telemetry")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    parsed_json = json.loads(msg.payload.decode('utf-8'))
    try: 
        print(parsed_json) 
        print(parsed_json['PCA1'])
        print(parsed_json['PCA2'])
        pca1=float(parsed_json['PCA1'])
        pca2=float(parsed_json['PCA2'])
        state = float(clf.predict([[pca1, pca2]]))
        print(state)
        pcaStatePredict['pcaStatePredict'] = state
        client.publish('v1/devices/me/telemetry', json.dumps(pcaStatePredict), 1)
        
    except: 
        print('Wrong Packet')

client = mqtt.Client()
client1 = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message#



client.connect(hostname, 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
