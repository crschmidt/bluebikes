#!/bin/bash -x

month=202208

mkdir output
wget -O output/$month.zip https://s3.amazonaws.com/hubway-data/$month-bluebikes-tripdata.zip
cd output
unzip $month.zip
echo ".mode csv
.import '$month-bluebikes-tripdata.csv' trips
.output startend_count.csv
select \"start station id\"||'-'||\"end station id\", count(*) from trips where \"start station id\"!=\"end station id\" group by 1" | sqlite3 trips.db
cd ..
mv output/startend_count.csv .
python route_shapefile.py
geo2topo usedroutes.geojson > usedroutes.topojson
python weight_segments.py