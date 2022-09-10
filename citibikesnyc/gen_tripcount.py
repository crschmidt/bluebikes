import sqlite3
import datetime
import csv

START_DATE = datetime.datetime(2021, 10, 1, 0, 0, 1)
END_DATE = datetime.datetime(2021, 11, 1, 0, 0, 0)
TIME_WINDOW = datetime.timedelta(minutes=15)

def run():
    # Load station to station route data
    pl = {}
    
    # Connect to db
    db = sqlite3.connect("trips.db")
    c = db.cursor()
    
    dt = START_DATE
    w = csv.writer(open('activetrips.csv', 'w'))
    w.writerow(['timestamp', 'count'])
    se = {}
    loops = 0
    while dt < END_DATE:
        
        q = "select count(*) from oct21 where started_at < '%s' and ended_at>'%s' and cast(strftime('%%s', ended_at)-strftime('%%s', started_at) as integer) < 3600" % (dt, dt)
        c.execute(q)
        data = c.fetchall()
        w.writerow([dt, data[0][0]])
        if loops % 10 == 0:
            print("Completed %s" % dt)
        loops += 1
        dt = dt + TIME_WINDOW

if __name__ == "__main__":
    run()
