import csv
import datetime
import json
import sqlite3
import zipfile

import polyline
from shapely.geometry import LineString

START_DATE = datetime.datetime(2022, 8, 1, 0, 0, 0)
END_DATE = datetime.datetime(2022, 8, 2, 0, 0, 0)
TIME_WINDOW = datetime.timedelta(minutes=2)


def fetch_polyline(zf, names, se):
    n = "%s.json" % se
    if not n in names:
        return None
    d = json.loads(zf.read("%s.json" % se))
    if not 'routes' in d:
        return None
    return polyline.decode(d['routes'][0]['geometry'], geojson=True)


def run():
    # Load station to station route data
    pl = {}
    zf = zipfile.ZipFile("routes.zip")
    zfnames = zf.namelist()
    # Connect to db
    db = sqlite3.connect("output/trips.db")
    c = db.cursor()
    dt = START_DATE
    w = csv.writer(open('out.csv', 'w'))
    w.writerow(['timestamp', 'lon', 'lat', 'bikeid'])
    se = {}
    loops = 0
    while dt < END_DATE:
        dt = dt + TIME_WINDOW
        c.execute("""
        select \"start station ID\", \"end station id\",
            tripduration, strftime('%%s', '%s')- \
                                   strftime('%%s', starttime), bikeid
        from trips
        where
            starttime < '%s' and stoptime>'%s' and cast(tripduration as integer) < 3600""" % (dt, dt, dt))
        data = c.fetchall()
        for row in data:
            s, e, duration, x, bikeid = row
            ip_dist = float(x)/float(duration)
            try:
                # Convert polyline to LineString + interpolate
                k = '%s-%s' % (s, e)
                if not k in pl:
                    l = fetch_polyline(zf, zfnames, k)
                    if not l:
                        continue
                    se[k] = l
                l = se[k]
                ip = LineString(l).interpolate(ip_dist, normalized=True)
                ts = dt-datetime.timedelta(hours=4)
                w.writerow([ts, ip.x, ip.y, bikeid])
            except KeyError as E:
                print(E)
                continue
        if loops % 10 == 0:
            print("Completed %s" % dt)
        loops += 1


if __name__ == "__main__":
    run()
