import zipfile

import os
import json

import csv

of = zipfile.ZipFile("polylines.zip", "w", allowZip64=True, compression=zipfile.ZIP_DEFLATED)

zf = zipfile.ZipFile("routes.zip") 
allroutes = zf.namelist()
for i in allroutes:
    if not ".json" in i: continue
    zf.read(i)
    f, t = i.strip("routes/").strip(".json").split("-")
    d = json.loads(zf.read(i))
    if not 'sets' in d:
        continue
    se = "%s-%s" % (f, t)
    polyline = d['sets'][0]['legs'][0]['paths'][0]['polyline']['data']
    of.writestr("%s.json" % se, polyline)
