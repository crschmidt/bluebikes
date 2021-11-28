#!/bin/sh

wget https://s3.amazonaws.com/hubway-data/202109-bluebikes-tripdata.zip
unzip 202109-bluebikes-tripdata.zip
sqlite3 trips.db < import.sql
wget https://housing.crschmidt.net/bikes/polylines.zip
unzip polylines.zip
