import csv
import time
import os
import json
import requests
import time

bad_stations = []
i = 0
r = csv.reader(open("route_pairs.csv"))
for row in r:
        s, s2, slat, slon, s2lat, s2lon, count = row
        if s in bad_stations or s2 in bad_stations:
            print "Skipping bad station"
            continue
        if s == s2: continue
        if os.path.exists("routes/%s_%s.json" % (s, s2)): 
            continue
        url = "http://127.0.0.1:5000/route/v1/bicycle/%s,%s;%s,%s?overview=full" % (float(slon), float(slat), float(s2lon), float(s2lat))
        req = None
        try:
            req = requests.post(url)
            json.loads(req.text)
        except Exception, E:
            print E
            if req:
                print req.text
            time.sleep(1)
            continue
        f = open("routes/%s_%s.json" % (s, s2), "w")
        f.write(req.text)
        f.close()
        req.close()
        i+=1
        if i % 100 == 0:
            print i
