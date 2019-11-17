import api_consumer
from map_updater.display import strip
from rpi_ws281x import Color
from typing import Tuple
import json

ALL_ROUTE_NUMBERS = ["6", "11", "13", "23"]

shown_route_numbers = ALL_ROUTE_NUMBERS # Updated by UI

with open('routes.json') as routes_file:
    routes = json.loads(routes_file.read())


class location(object):
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long


def distance(pos1: location, pos2: location):
    diff_x = pos1.lat - pos2.lat
    diff_y = pos1.long - pos2.long
    return (diff_x**2 + diff_y**2)**0.5

def find_nearest_stop(route: str, bus_location: location):
    '''
    Yes, Jeff, this is wrong. I _do_ understand that lines of latitude and
    longitude are not perpendicular, nor square. However, Duluth has quite a
    few other issues like hills, which present much larger discrepancies than
    the curvature of the Earth.

    Plus, the Earth is flat anyway. Wake up, sheeple.
    xkcd.com/{1013,1318}
    '''
    closest_stop = route_stops[route][0]
    for route in route_stops:
        for stop in route:
            if distance(bus_location, stop) < distance(bus_location, closest_stop):
                closest_stop = stop
    return closest_stop

def update_map():
    for i in range(strip.numPixels()): # or LED_COUNT
        strip.setPixelColor(i, Color(0,0,0))

    # TODO: set colors per-route

    # If we're only showing one map, highlight all the stops
    if len(shown_routes) is 1:
        for stop in routes[shown_routes[0]]:
            strip.setPixelColor(stop, Color(2,10,2))
    #for bus in api_consumer.get_buses(shown_routes):
    #    bus_location = location(bus.lat, bus.long)
    #    show_stop(find_nearest_stop(bus_location))
    strip.setPixelColor(20, Color(255,255,255))
    strip.show()

def clear_map():
    display.clear()

def show_route(route: str):
    global shown_routes
    shown_routes = [route]
    update_map()

def show_all_routes():
    global shown_routes
    shown_routes = ALL_ROUTES
    update_map()
