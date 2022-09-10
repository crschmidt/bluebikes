import json

doc = json.load(open("usedroutes.topojson"))
geoms = doc['objects']['usedroutes']['geometries']
a_weights = {}
for g in geoms:
    for arc in g['arcs']:
        if arc < 0: arc = ~arc
        a_weights[arc] = a_weights.get(arc, 0)+g['properties']['trips']
c = {'type':'FeatureCollection', 'features':[]}
for k, v in a_weights.items(): 
    f = {'type':'Feature', 'properties': {'trips': v}, 'geometry':{'type':'LineString', 'coordinates': doc['arcs'][k]}}
    #if v > 10000:
    #    print(doc['arcs'][k], v)
    c['features'].append(f)

json.dump(c, open("toporoutes.geojson", "w"))
#print(doc['arcs'])