import json
import csv
import datetime

r = csv.reader(open("../../ebike_data.txt"))

bikes = {}

trips = []

def compute_minutes_between_times(data):
    """
    Computes the number of minutes between start and end times in a given data dictionary.

    Parameters:
    data (dict): A dictionary containing 'start_time' and 'end_time' keys with ISO formatted datetime strings.

    Returns:
    int: The number of minutes between the start and end times.
    """
    from datetime import datetime

    # Extracting start and end times from the data
    start_time_str = data['start_time'].replace('Z', '+00:00')
    end_time_str = data['end_time'].replace('Z', '+00:00')

    # Parsing the start and end times
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)

    # Calculating the difference in minutes
    return int((end_time - start_time).total_seconds() / 60)


for row in r:
    if len(row) == 4:
        date, station, bike, battery = row
    else:
        date, _, bike, battery, station = row
    if not bike in bikes:
        bikes[bike] = {'station': station, 'battery': battery, 'date': date}
    if bikes[bike]['station'] != station and bikes[bike]['battery'] != battery:
#        print(bikes[bike]['station'] != station,  bikes[bike]['battery'] != battery)
        trips.append({'start_batt': bikes[bike]['battery'], 'end_batt': battery, 'start_time': bikes[bike]['date'], 'end_time': date, 'start': bikes[bike]['station'], 'end': station, 'bike': bike})
    bikes[bike] = {'station': station, 'battery': battery, 'date': date}
s = 0
b = 0
for i in trips:
    m = compute_minutes_between_times(i)
    bat = int(i['start_batt']) - int(i['end_batt'])
    i['batt_min'] = float(bat)/m
    i['min'] = m
    s+= m
    b += bat
    print(i)
print(len(trips), s, b)
json.dump(trips, open("trips.json", "w"))
