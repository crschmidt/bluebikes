import sqlite3
import datetime
import zipfile
import polyline
import json
from shapely.geometry import LineString
import csv

START_DATE = datetime.datetime(2021, 10, 1, 0, 0, 0)
END_DATE = datetime.datetime(2021, 11, 1, 0, 0, 0)
TIME_WINDOW = datetime.timedelta(minutes=4)

def run():
    # Load station to station route data
    pl = {}
    r = csv.reader(open("polylines-nyc.csv"))
    r.next()
    for row in r:
        se, geom = row
        pl[se] = geom
    
    # Connect to db
    db = sqlite3.connect("trips.db")
    c = db.cursor()
    
    dt = START_DATE
    fn = dt.strftime("%Y%m%d")
    w = csv.writer(open('points-%s.csv' % fn, 'w'))
    w.writerow(['timestamp', 'lon', 'lat', 'bikeid'])
    se = {}
    loops = 0
    while dt < END_DATE:
        dt = dt + TIME_WINDOW
        if dt.strftime("%Y%m%d") != fn:
            fn = dt.strftime("%Y%m%d")
            w = csv.writer(open('points-%s.csv' % fn, 'w'))
            w.writerow(['timestamp', 'lon', 'lat', 'bikeid'])
            del se
            se = {}

        q = "select start_station_id, end_station_id, strftime('%%s', ended_at)-strftime('%%s', started_at) as tripduration, strftime('%%s', '%s')-strftime('%%s', started_at), start_station_id from oct21 where started_at < '%s' and ended_at>'%s' and cast(tripduration as integer) < 3600 and end_station_id!='' and start_station_id!='' and end_station_id!=start_station_id" % (dt, dt, dt)
        found = 0
        i = 0
        c.execute(q)
        data = c.fetchall()
        for row in data:
            i += 1
            s, e, duration, x, bikeid = row
            ip_dist = float(x)/float(duration)
    
            try:
                # Convert polyline to LineString + interpolate
                k = '%s_%s' % (s, e)
                if not k in se:
                    if not k in pl: 
                        print k
                        continue
                    l = polyline.decode(pl[k], geojson=True)
                    se[k] = l
                l = se[k]
                ip = LineString(l).interpolate(ip_dist, normalized=True)
                w.writerow([dt, ip.x, ip.y, bikeid])
            except KeyError:
                continue
            found += 1
        if found != i:
            print "Found %s out of %s" % (found, i)
        if loops % 10 == 0:
            print "Completed %s" % dt
        loops += 1

if __name__ == "__main__":
    run()
