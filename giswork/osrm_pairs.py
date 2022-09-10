import time
import os
import json

stations = {}

data = json.load(open("station_information.json"))
for s in data['data']['stations']:
    if s['capacity'] > 0:
        id, lat, lon = s['station_id'], s['lat'], s['lon']
        stations[id] = [lat, lon]
print(len(stations))

#import csv
#r = csv.reader(open("current_bluebikes_stations.csv"))
#r.next()
#r.next()
# Number,Name,Latitude,Longitude,District,Public,Total docks,year
#for row in r:
#    id, _, lat, lon, _, _, docks, _ = row
#    stations[id] = [lat, lon]


import requests

import time

#bad_stations =['171', '182', '213', '377', '46', '471'] 
bad_stations = []
i = 0
station_pairs = []
def run_one(pair):

        global i, stations
        s, s2 = pair
        url = "http://127.0.0.1:5000/route/v1/bicycle/%s,%s;%s,%s?overview=full" % (stations[s][1], stations[s][0], stations[s2][1], stations[s2][0])
        
        try:
            r = requests.post(url)
            json.loads(r.text)
        except Exception as E:
            print (E)
            time.sleep(1)
            return
        f = open("routes2/%s-%s.json" % (s, s2), "w")
        f.write(r.text)
        f.close()
        i+=1
        if i % 500 == 0:
            print(i)

for s in stations:
    for s2 in stations:
        if s in bad_stations or s2 in bad_stations:
            print("Skipping bad station")
            continue
        if s == s2: continue
        if os.path.exists("routes2/%s-%s.json" % (s, s2)): 
            continue
        station_pairs.append([s, s2])
import multiprocessing
pool = multiprocessing.Pool(8)
pool.map(run_one, station_pairs)