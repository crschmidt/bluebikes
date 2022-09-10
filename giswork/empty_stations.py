import json

station_map = {}
info = json.load(open('station_information.json'))
for i in info['data']['stations']:
    station_map[i['station_id']] = i
status = json.load(open("station_status.json"))
for i in status['data']['stations']:
    if i['station_status'] != "active":
        continue
    print(",".join([str(i['num_bikes_available']), station_map[i['station_id']]['name']]))
