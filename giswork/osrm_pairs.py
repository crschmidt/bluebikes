import json
import multiprocessing
import os
import time

import requests

OUTPUTDIR = "routes"
BAD_STATIONS = []

stations = {}


def run_one(pair):

    global stations
    s, s2 = pair
    if not s in stations or not s2 in stations:
        return
    url = "http://127.0.0.1:5000/route/v1/bicycle/%s,%s;%s,%s?overview=full" % (
        stations[s][1], stations[s][0], stations[s2][1], stations[s2][0])
    try:
        r = requests.post(url)
        json.loads(r.text)
    except Exception as E:
        print(E)
        time.sleep(1)
        return
    f = open("%s/%s-%s.json" % (OUTPUTDIR, s, s2), "w")
    f.write(r.text)
    f.close()


def should_fetch_station(s, s2):
    if s in BAD_STATIONS or s2 in BAD_STATIONS:
        print("Skipping bad station in pair %s, %s" % (s, s2))
        return False
    if s == s2:
        return False
    if os.path.exists("%s/%s-%s.json" % (OUTPUTDIR, s, s2)):
        return False
    return True


def run():

    if not os.path.exists(OUTPUTDIR):
        os.mkdir(OUTPUTDIR)

    data = json.load(open("station_information.json"))
    for s in data['data']['stations']:
        # if s['capacity']:
        id, lat, lon = s['station_id'], s['lat'], s['lon']
        stations[id] = [lat, lon]
    print(len(stations))
   # return

    station_pairs = []

    if os.path.exists('startend_count.csv'):
        for i in open("startend_count.csv"):
            startend, count = i.strip().split(",")
            s, s2 = startend.split("-")
            if should_fetch_station(s, s2):
                station_pairs.append([s, s2])

    else:
        for s in stations:
            for s2 in stations:
                if should_fetch_station(s, s2):
                    station_pairs.append([s, s2])

    print(len(station_pairs))
    pool = multiprocessing.Pool(16)
    pool.map(run_one, station_pairs)


if __name__ == "__main__":
    run()
    # workaround for connection aborts -- just run it again
    time.sleep(10)
    run()
