#!/bin/sh

wget https://s3.amazonaws.com/tripdata/JC-202110-citibike-tripdata.csv.zip
wget https://s3.amazonaws.com/tripdata/202110-citibike-tripdata.csv.zip

wget https://housing.crschmidt.net/bikes/polylines-nyc.zip

unzip 202110-citibike-tripdata.csv.zip
unzip JC-202110-citibike-tripdata.csv.zip
unzip polylines-nyc.zip
sqlite3 trips.db < import.sql
