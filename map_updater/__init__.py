import api_consumer
from .display import strip
from rpi_ws281x import Color
from typing import Tuple
import json
import os

ALL_ROUTE_NUMBERS = ["6", "11", "11K", "13", "23"]



def distance_between(obj1, obj2):
    diff_x = obj1['lat'] - obj2['lat']
    diff_y = obj1['long'] - obj2['long']
    return (diff_x**2 + diff_y**2)**0.5


class MapUpdater:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'routes.json')) as routes_file:
            self.routes = json.loads(routes_file.read())
        self.shown_route_numbers = ALL_ROUTE_NUMBERS # Updated by UI

    def find_nearest_stop(self, route_name: str, bus_location):
        '''
        Yes, Jeff, this is wrong. I _do_ understand that lines of latitude and
        longitude are not perpendicular, nor square. However, Duluth has quite a
        few other issues like hills, which present much larger discrepancies than
        the curvature of the Earth.

        Plus, the Earth is flat anyway. Wake up, sheeple.
        xkcd.com/{1013,1318}
        '''
        route = self.routes[route_name]
        closest_stop = route['stops'][0]
        for stop in route['stops']:
            if distance_between(bus_location, stop) < distance_between(bus_location, closest_stop):
                closest_stop = stop
        return closest_stop

    def update_map(self):
        # Start with blank board
        for i in range(strip.numPixels()):  # or LED_COUNT
            strip.setPixelColor(i, Color(0,0,0))

        # If we're only showing one route, highlight all the stops on that route
        if len(self.shown_route_numbers) is 1:
            for stop in self.routes[self.shown_route_numbers[0]]['stops']:
                strip.setPixelColor(stop['led'], Color(4, 4, 4))

        # Show vehicles
        for bus in api_consumer.get_buses(*self.shown_route_numbers):
            print(bus)
            bus_led = self.find_nearest_stop(bus['route'], bus)['led']
            bus_color = self.routes[bus['route']]['color']
            bus_color = Color(bus_color[1], bus_color[0], bus_color[2])  # GRB
            strip.setPixelColor(bus_led, bus_color)

        # Finally, flush the changes to the board!
        strip.show()

    def show_route(self, route: str):
        self.shown_route_numbers = [route]
        if route == "11":
            self.shown_route_numbers = ["11K"] # Hackety hack hack, TODO: remove
        print("Showing %s" % self.shown_route_numbers)

        self.update_map()

    def show_all_routes(self):
        self.shown_route_numbers = ALL_ROUTE_NUMBERS
        print("Showing %s" % self.shown_route_numbers)
        self.update_map()
