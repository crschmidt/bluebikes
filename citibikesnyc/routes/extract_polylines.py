import zipfile

import os
import json

import csv

w = csv.writer(open("polylines-nyc.csv", "w"))
w.writerow(["start_end", "polyline"]) 
allroutes = os.listdir("routes")
for i in allroutes:
    if not ".json" in i: continue
    fh = open("routes/%s" % i)
    f, t = i.strip(".json").split("_")
    try:
        d = json.loads(fh.read())
    except Exception, E:
        print i
        raise E
    if not 'code' in d or not d['code'] == 'Ok':
        print 'skipping', i
        continue
    se = "%s_%s" % (f, t)
    polyline = d['routes'][0]['geometry']
    w.writerow([se, polyline])
