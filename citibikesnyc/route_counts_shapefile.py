import csv
import sqlite3
import fiona
from fiona.crs import from_epsg
import polyline
pl = {}
r = csv.reader(open("polylines-nyc.csv"))
r.next()
for row in r:
    se, geom = row
    pl[se] = geom

db = sqlite3.connect("trips.db")
c = db.cursor()
c.execute("select start_station_id, end_station_id, count(*) as c from oct21 where start_station_id != '' and end_station_id != '' and start_station_id!=end_station_id group by 1,2 order by c desc")

with fiona.open("routes.shp", "w", crs=from_epsg(4326), driver='ESRI Shapefile',
schema={
    'geometry': 'LineString',
'properties':{
    'start': 'str:24',
    'end': 'str:24',
    'trips': 'int'}}) as output:
    ptypes = {k: fiona.prop_type(v) for k, v in output.schema['properties'].items()}
    for row in c.fetchall():

        s, e, c = row
        k = '%s_%s' % (s, e)
        if not k in se:
            if not k in pl: 
                print("Missing route", k)
                continue
        output.write({
            'type':'Feature', 'geometry': {
            'type':'LineString',
            'coordinates': polyline.decode(pl[k], geojson=True)},
            'properties': {'start': s, 'end':e, 'trips': c}
        })
