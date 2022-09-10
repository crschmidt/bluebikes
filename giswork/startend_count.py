import csv
#"tripduration","starttime","stoptime","start station id","start station name","start station latitude","start station longitude","end station id","end station name","end station latitude","end station longitude","bikeid","usertype","postal code"

r = csv.DictReader(open("202207-bluebikes-tripdata.csv"))
for row in r:
        print(row)
