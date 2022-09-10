import os
import json

stations = {}

data = json.load(open("station_information.json"))
for s in data['data']['stations']:
    if s['capacity'] > 0:
        id, lat, lon = s['station_id'], s['lat'], s['lon']
        stations[id] = [lat, lon]
print(len(stations))

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

bad_stations =['171', '182', '213', '377', '46', '471']  

for s in stations:
    for s2 in stations:
        print(s, s2)
        if s in bad_stations or s2 in bad_stations:
            print("Skipping bad station")
            continue
        if s == s2: continue
        if os.path.exists("routes/%s-%s.json" % (s, s2)): 
            print("Exists")
            continue
        r = requests.post(url, headers=headers, data='{"sets":[{"elements":[{"element_type":1,"waypoint":{"point":{"lat":%.6f,"lng":%.6f}}},{"element_type":1,"waypoint":{"point":{"lat":%.6f,"lng":%.6f}}}],"preferences":{"popularity":0.5,"elevation":0,"route_type":1,"route_sub_type":5,"straight_line":false}}]}' % (stations[s][0], stations[s][1], stations[s2][0], stations[s2][1]))
        try:
            json.loads(r.text)
        except Exception as E:
            print(E, r.text)
            break
        f = open("routes/%s-%s.json" % (s, s2), "w")
        f.write(r.text)
        f.close()
