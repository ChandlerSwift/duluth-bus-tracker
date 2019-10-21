#!/usr/bin/python3
from flask import Flask, send_file, redirect
import map_updater
import threading
import time

app = Flask(__name__)

MAP_UPDATE_INTERVAL = 1 # second

@app.route('/')
def index():
	return redirect('static/')

next_call = time.time() + MAP_UPDATE_INTERVAL
def schedule_next_update():
	map_updater.update_map()

	# schedule next update
	global next_call
	next_call += MAP_UPDATE_INTERVAL
	threading.Timer(next_call - time.time(), schedule_next_update).start()

@app.route('/api/show_route/<int:route>')
def show_route(route: int):
	map_updater.show_route(route)

if __name__ == '__main__':
	schedule_next_update()
	app.run()
