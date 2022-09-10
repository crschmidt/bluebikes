import json
import os
import zipfile
from csv import DictReader

import fiona
import polyline
from fiona.crs import from_epsg

tripcount = {}
for i in open("startend_count.csv"):
    startend, count = i.strip().split(",")
    tripcount[startend] = count
print(len(tripcount))
with fiona.open("usedroutes.geojson", "w", crs=from_epsg(4326), driver='GeoJSON',
                schema={
    'geometry': 'LineString',
    'properties': {
        'start': 'str:24',
        'end': 'str:24',
        'trips': 'int'}}) as output:
    ptypes = {k: fiona.prop_type(v)
              for k, v in output.schema['properties'].items()}
    zf = zipfile.ZipFile("routes.zip")
    allroutes = zf.namelist()
    for i in allroutes:
        if not ".json" in i:
            continue
        zf.read(i)
        f, t = i.strip("routes/").strip(".json").split("-")
        # print(f,t)
        d = json.loads(zf.read(i))
        if not 'routes' in d:
            continue
        se = "%s-%s" % (f, t)
        if not se in tripcount:
            continue
        output.write({
            'type': 'Feature', 'geometry': {
                'type': 'LineString',
                'coordinates': polyline.decode(d['routes'][0]['geometry'], geojson=True)},
            'properties': {'start': f, 'end': t, 'trips': tripcount.get(se, 0)}
        })
