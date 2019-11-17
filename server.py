#!/usr/bin/python3
from flask import Flask, send_from_directory
from map_updater import MapUpdater
import api_consumer
import threading
import time

app = Flask(__name__)

MAP_UPDATE_INTERVAL = 5 # second
RELEVANT_BUSES = ["6", "11", "11K", "13", "23"]

map_updater = MapUpdater()

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def index(path):
	return send_from_directory('static', path)

next_call = time.time() + MAP_UPDATE_INTERVAL
def schedule_next_update():
	map_updater.update_map()

	# schedule next update
	global next_call
	next_call += MAP_UPDATE_INTERVAL
	threading.Timer(next_call - time.time(), schedule_next_update).start()

@app.route('/api/get-upcoming-departures')
def get_upcoming_departures():
	return "[]"
	return api_consumer.get_upcoming_departures(RELEVANT_BUSES)

@app.route('/api/show_route/<route>')
def show_route(route: str):
	map_updater.show_route(route)

@app.route('/api/show_all_routes')
def show_all_routes():
	map_updater.show_all_routes()

if __name__ == '__main__':
	schedule_next_update()
	app.run()
