import sqlite3
import datetime
import zipfile
import polyline
import json
from shapely.geometry import LineString
import csv

START_DATE = datetime.datetime(2021, 9, 10, 0, 0, 0)
END_DATE = datetime.datetime(2021, 9, 12, 0, 0, 0)
TIME_WINDOW = datetime.timedelta(minutes=2)

def run():
    # Load station to station route data
    pl = {}
    r = csv.reader(open("polylines.csv"))
    r.next()
    for row in r:
        se, geom = row
        pl[se] = geom
    # Connect to db
    db = sqlite3.connect("trips.db")
    c = db.cursor()
    dt = START_DATE
    w = csv.writer(open('out.csv', 'w'))
    w.writerow(['timestamp', 'lon', 'lat', 'bikeid'])
    se = {}
    loops = 0
    while dt < END_DATE:
        dt = dt + TIME_WINDOW
        c.execute("select \"start station ID\", \"end station id\", tripduration, strftime('%%s', '%s')-strftime('%%s', starttime), bikeid from sep21 where starttime < '%s' and stoptime>'%s' and cast(tripduration as integer) < 3600" % (dt, dt, dt))
        data = c.fetchall()
        for row in data:
            s, e, duration, x, bikeid = row
            ip_dist = float(x)/float(duration)
            try:
                # Convert polyline to LineString + interpolate
                k = '%s-%s' % (s, e)
                if not k in se:
                    if not k in pl: continue
                    l = polyline.decode(pl[k], geojson=True)
                    se[k] = l
                l = se[k]
                ip = LineString(l).interpolate(ip_dist, normalized=True)
                ts = dt-datetime.timedelta(hours=4)
                w.writerow([ts, ip.x, ip.y, bikeid])
            except KeyError:
                continue
        if loops % 10 == 0:
            print "Completed %s" % dt
        loops += 1

if __name__ == "__main__":
    run()
