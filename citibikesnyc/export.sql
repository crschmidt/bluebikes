.mode csv
.output route-pairs.csv
select start_station_id, end_station_id, start_lat, start_lng, end_lat, end_lng, count(*) as c from oct21 where start_station_id != '' and end_station_id != '' group by 1,2 order by c desc;
