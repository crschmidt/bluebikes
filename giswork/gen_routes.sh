#!/bin/bash -x

wget https://gbfs.bluebikes.com/gbfs/en/station_information.json
wget http://download.geofabrik.de/north-america/us/massachusetts-latest.osm.pbf
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/bicycle.lua /data/massachusetts-latest.osm.pbf
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/massachusetts-latest.osrm
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/massachusetts-latest.osrm
docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/massachusetts-latest.osrm
python osrm_pairs.py
cd routes
zip -0rq ../routes.zip .

