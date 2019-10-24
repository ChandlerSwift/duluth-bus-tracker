from typing import List

VEHICLE_POSITION_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json'

def get_buses(*routes: str):
    """
    Returns a list of bus objects and their locations. The argument routes
    must be strings because of routes like the "11" vs "11K".
    """
    pass
