import api_consumer
import map_updater.display

ALL_ROUTES = ["6", "11", "13", "23"]

shown_routes = []

route_stops = {
    "6": [],
    "11": [],
    "13": [{"lat":0,"long":0,"led":x} for x in range(50)],
    "23": [],
}

# stop = {
#   "led": 1,
#   "lat": 54.2533710,
#   "long": 62.8501745,
#   "name": "12th Ave and 4th St",
# }


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

    Plus, the Earth is flat anyway.
    '''
    closest_stop = route_stops[route][0]
    for route in route_stops:
        for stop in route:
            if distance(bus_location, stop) < distance(bus_location, closest_stop):
                closest_stop = stop
    return closest_stop

def update_map():
    clear_map()

    # TODO: set colors

    # If we're only showing one map, highlight all the stops
    if len(shown_routes) is 1:
        for stop in route_stops[shown_routes[0]]:
            show_stop(stop, 0.1)
    #for bus in api_consumer.get_buses(shown_routes):
    #    bus_location = location(bus.lat, bus.long)
    #    show_stop(find_nearest_stop(bus_location))
    show_stop({"led":20})

def clear_map():
    display.clear()

def show_stop(stop, brightness: float = 1.0):
    display.show(stop.led, (255 * brightness, 255 * brightness, 255 * brightness))

def show_route(route: str):
    global shown_routes
    shown_routes = [route]
    update_map()

def show_all_routes():
    global shown_routes
    shown_routes = ALL_ROUTES
    update_map()
