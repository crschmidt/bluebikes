.mode csv
.import '202109-bluebikes-tripdata.csv' sep21
create index sep21_starttime on sep21 (starttime);
