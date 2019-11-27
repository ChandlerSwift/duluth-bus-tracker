#!/bin/bash

#########################
#if false; then
#########################

if test -f database.sqlite; then
    read -n 1 -r -p "Warning, database exists. Data may be doubly imported. Do you want to remove this file? [y/n] "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm database.sqlite
    fi
fi

echo "Downloading..."
wget -q http://duluthtransit.com/gtf/google_transit.zip

echo "Unzipping..."
unzip google_transit.zip

echo "Importing..."
sqlite3 database.sqlite <<"EOF"
.mode csv
.import routes.txt routes
.import stop_times.txt stop_times
.import stops.txt stops
.import trips.txt trips
EOF

echo "Import complete!"

if test -f stop_data; then
    read -n 1 -r -p "Warning, stop data file exists. Data may be doubly imported. Do you want to remove this file? [y/n] "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm stop_data
    fi
fi

echo "Parsing for stop data..."
for route in 6 11 11K 13 23; do
    echo "    Parsing route $route..."
    sqlite3 database.sqlite >> tmp_stop_data <<EOF
.mode csv
select '$route' as route,stop_name,stop_id,stop_lat,stop_lon from stops where stop_id in (
    select stop_id from stop_times where trip_id = (
        select trip_id from trips where route_id = '$route' LIMIT 1
    )
);
EOF
done
echo "Parsing complete!"

echo "route,name,id,lat,long" > stop_data # create header row

echo "Filtering duplicate routes..."
cat tmp_stop_data | sort | uniq >> stop_data
rm tmp_stop_data

echo "Processing complete! $(cat stop_data | wc -l) stops processed."

#############################
#fi
#############################

echo "Exporting stop data as JSON..."
# We can't just python<<EOF because we need stdin for LED assignment.
cat > json_generator.py <<EOF
import csv
import json

filename=input("Where would you like to save the json file? ")

with open('stop_data') as stop_data_file:
    reader = csv.DictReader(stop_data_file)
    stops = list(reader)

for stop in stops:
    stop_led = input(stop['name'].ljust(20) + ": ")
    stop['led'] = int(stop_led) if stop_led is not "" else 0
    stop['lat'] = float(stop['lat'])
    stop['long'] = float(stop['long'])

with open('routes.txt') as routes_file:
    reader = csv.DictReader(routes_file)
    routes = [route for route in reader if route['route_id'] in ['6', '13', '23', '11', '11K']]

output_routes = {}
for route in routes:
    output_routes[route['route_id']] = {
        'color': [int(route['route_color'][i:i+2], 16) for i in (0, 2, 4)],
        'name': route['route_long_name'],
        'stops': []
    }
    for stop in stops:
        if stop['route'] == route['route_id']:
            output_routes[route['route_id']]['stops'].append(stop)
with open(filename, 'w') as f:
 f.write(json.dumps(output_routes))
EOF
python3 json_generator.py

echo "Cleaning up..."
rm -f agency.txt calendar_dates.txt calendar.txt feed_info.txt \
    google_transit.zip routes.txt shapes.txt stop_times.txt stops.txt \
    trips.txt json_generator.py stop_data google.transit.zip.* database.sqlite
