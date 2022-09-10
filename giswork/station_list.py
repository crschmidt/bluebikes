import json

d = json.load(open("station_information.json"))
for i in d['data']['stations']:
    print("%.5f,%.5f" % (i['lat'], i['lon']))
