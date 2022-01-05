import polyline
import os
import json
allroutes = os.listdir("routes")
fc = {'type':'FeatureCollection', 'features': []}
f = open("routes.geojson", "w")
for i in allroutes:
#    if not i.startswith("296-"): continue
    d = json.load(open("routes/%s" % i))
    if not 'sets' in d:
        continue
    fc['features'].append({
        'type':'Feature', 'geometry': {
        'type':'LineString',
        'coordinates': polyline.decode(d['sets'][0]['legs'][0]['paths'][0]['polyline']['data'], geojson=True)},
    })
json.dump(fc, f)
