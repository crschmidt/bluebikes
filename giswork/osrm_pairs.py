import time
import os
import json

stations = {}

data = json.load(open("station_information.json"))
for s in data['data']['stations']:
    if s['capacity'] > 0:
        id, lat, lon = s['station_id'], s['lat'], s['lon']
        stations[id] = [lat, lon]
print len(stations)

import requests
url = 'https://www.strava.com/frontend/routemaster/bulk_route'  
headers = { 
 'authority': 'www.strava.com',
 'accept': 'application/json',   
 'content-type': 'application/json;charset=UTF-8',   
 'x-csrf-token': '6A27m/946XEbnsr0fLymJzk3gMTb5zlqZFUQ0PmIXrJAs8b8PeU47QWoejNyUI5wBCFSzaby7DEsfPVjLiRdkg==',         
 'cookie': '_strava4_session=ggt6un0df2t24q23dl0na9sboloa9fie; CloudFront-Key-Pair-Id=APKAIDPUN4QMG7VUQPSA; _sp_ses.047d=*; ',
}
import time

#bad_stations =['171', '182', '213', '377', '46', '471'] 
bad_stations = []
i = 0
for s in stations:
    for s2 in stations:
        if s in bad_stations or s2 in bad_stations:
            print "Skipping bad station"
            continue
        if s == s2: continue
        if os.path.exists("routes2/%s-%s.json" % (s, s2)): 
            continue
        url = "http://127.0.0.1:5000/route/v1/bicycle/%s,%s;%s,%s" % (stations[s][1], stations[s][0], stations[s2][1], stations[s2][0])
        
        try:
            r = requests.post(url)
            json.loads(r.text)
        except Exception, E:
            print E
            print r.text
            time.sleep(1)
            continue
        f = open("routes2/%s-%s.json" % (s, s2), "w")
        f.write(r.text)
        f.close()
        i+=1
        if i % 100 == 0:
            print i
