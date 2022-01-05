import zipfile
from csv import DictReader
import fiona
from fiona.crs import from_epsg

import polyline
import os
import json

tripcount = {}
for i in open("startend_count.csv"):
    startend, count = i.strip().split(",")
    tripcount[startend] = count

with fiona.open("usedroutes.shp", "w", crs=from_epsg(4326), driver='ESRI Shapefile',
schema={
    'geometry': 'LineString',
'properties':{
    'start': 'str:24',
    'end': 'str:24',
    'trips': 'int'}}) as output:
    ptypes = {k: fiona.prop_type(v) for k, v in output.schema['properties'].items()}
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
        if not se in tripcount:
            continue
        output.write({
            'type':'Feature', 'geometry': {
            'type':'LineString',
            'coordinates': polyline.decode(d['sets'][0]['legs'][0]['paths'][0]['polyline']['data'], geojson=True)},
            'properties': {'start': f, 'end':t, 'trips': tripcount.get(se, 0)}
        })
