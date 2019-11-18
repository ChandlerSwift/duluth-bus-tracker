from typing import List
import json
import urllib.request
import time

VEHICLE_POSITION_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json'
UPCOMING_STOP_TIMES_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.json'

def make_bus_object(bus):
    new_bus = {}
    new_bus['lat'] = bus['vehicle']['position']['latitude']
    new_bus['long'] = bus['vehicle']['position']['longitude']
    new_bus['route'] = bus['vehicle']['trip']['route_id']
    return new_bus

def get_buses(*routes: str):
    """
    Returns a list of bus objects and their locations. The argument routes
    must be strings because of routes like the "11" vs "11K".
    """
    with urllib.request.urlopen(VEHICLE_POSITION_DATA_URL) as url:
        buses = json.loads(url.read().decode())['entity']

    print(routes)
    relevant_buses = []
    for bus in buses:
        if bus['vehicle']['trip']['route_id'] in routes:
            relevant_buses.append(make_bus_object(bus))
    return relevant_buses

def get_bus_data():
    bus_data = None
    json.loads("")
    return bus_data

def get_upcoming_departures(*routes_to_check: str):
    upcoming_departures = []
    stop_detail = { # TODO: Figure out directions for the #23
        # 04 St & 12 AE:
        '2-6688': {'13': 'From Downtown', '23': 'TODO: ???'},
        '1-6688': {'13': 'To Downtown', '23': 'TODO: ???'},
        # 09 St & 12 AE:
        '2-6926': {'11': 'From Downtown', '11K': 'From Downtown', '23': 'TODO: ???'},
        '1-6926': {'11': 'To Downtown', '11K': 'From Downtown', '23': 'TODO: ???'},
        # Superior St & 12 AE:
        '2-8008': {'6': 'From Downtown'},
        '1-6459': {'6': 'To Downtown'},
        }
    with urllib.request.urlopen(UPCOMING_STOP_TIMES_DATA_URL) as url:
        route_data = json.loads(url.read().decode())['entity']
    for route in route_data:
        route_id = route['trip_update']['trip']['route_id']
        if route_id in routes_to_check:
            for stop in route['trip_update']['stop_time_update']:
                if stop['stop_id'] in stop_detail.keys(): # one we care about
                    if stop['departure']['time'] > time.time(): # not in the past
                        upcoming_departures.append({
                            'route': route_id,
                            'direction': stop_detail[stop['stop_id']][route_id], 
                            'time': stop['departure']['time']
                            })
    return upcoming_departures

def latest_of(upcoming_departures):
    """
    for each departure in the list:
    if there isn't an equivalent departure already in the new list
        then add it
    otherwise (if there _is_ a equivalent departure in the new list)
        then if this one is newer
            replace that one than this one
        otherwise
            don't do anything
    return the new list
    """
    filtered_upcoming_departures = []
    for upcoming_departure in upcoming_departures:
        duplicate = None
        for filtered_upcoming_departure in filtered_upcoming_departures:
            if upcoming_departure['route'] == filtered_upcoming_departure['route'] \
                and upcoming_departure['direction'] == filtered_upcoming_departure['direction']:
                duplicate = filtered_upcoming_departure
        if duplicate == None:
            filtered_upcoming_departures.append(upcoming_departure)
        else:
            if duplicate['time'] > upcoming_departure['time']:
                duplicate = upcoming_departure
    return filtered_upcoming_departures

