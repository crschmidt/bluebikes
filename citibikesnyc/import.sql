.mode csv
.import "202110-citibike-tripdata.csv" oct21
.import "JC-202110-citibike-tripdata.csv" oct21jc
insert into oct21 select * from oct21jc;
