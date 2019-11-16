from typing import List
import json
import urllib.request

VEHICLE_POSITION_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json'
UPCOMING_STOP_TIMES_DATA_URL = ''

def make_bus_object(bus):
    new_bus = {}
    new_bus['lat'] = bus['vehicle']['position']['latitude']
    new_bus['long'] = bus['vehicle']['position']['longitude']
    new_bus['route'] = bus['vehicle']['trip']['route_id']]
    return new_bus

def get_buses(*routes: str):
    """
    Returns a list of bus objects and their locations. The argument routes
    must be strings because of routes like the "11" vs "11K".
    """
    with urllib.request.urlopen(VEHICLE_POSITION_DATA_URL) as url:
        buses = json.loads(url.read())['entity']

    relevant_buses = []
    for bus in buses:
        if bus['vehicle']['trip'] in routes:
            relevant_buses.append(make_bus_object(bus))
    return relevant_buses

def get_bus_data():
    bus_data = None
    json.loads()
    return bus_data

def get_upcoming_departures(*routes: str):
    ...
