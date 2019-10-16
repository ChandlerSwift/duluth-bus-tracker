import json
import threading
from socket import *
import sys
import requests
from urllib import request

# Idk how many of these we will actually need, we just trying stuff

HOST = ''
PORT = 8989

VEHICLE_POSITION_DATA_URL = r'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json'

def download_file_info(VEHICLE_POSITION_DATA_URL):
	file_open = request.urlopen(VEHICLE_POSITION_DATA_URL) # Open the file

	file_info = file_open.read() # Read the file

	file_info_str = str(file_info) # convert to string

	file_lines = file_info_str.split('\\n') # Actually make it readable

	

