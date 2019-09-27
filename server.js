const request = require('request');
const ws = require('ws');

const UPDATE_INTERVAL_MS = 500;
const VEHICLE_POSITION_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json';
const wss = new WebSocket.Server({ port: 8080 });

let connections = [];

wss.on('connection', function connection(conn) {
	conn.on('message', function incoming(message) {
		// discard messages (for now?)
	});

	connections.push(conn);
});

let buses = [];

/** Checks for updated bus locations, and sends updates to all connected clients */
function updateBusLocations() {
	let vehicles = getVehicles();
	let relevantVehicles = filterVehiclesByRoute(vehicles, [6, 13, 23]);
	for (let bus of relevantVehicles) {
		if (magicMethodForBusThatHasChanged()) { // TODO
			for (let conn of connections) {
				const update = '' // TODO
				conn.send(update);
			}
		}
	}
}

/** Downloads the location of all buses, returns as an array of buses */
function getVehicles() {
	request(VEHICLE_POSITION_DATA_URL, function(error, response, body) { 
		vehicle_data = JSON.parse(body); 
	});
	return vehicle_data.entity;
}

/** Given an array of buses and an array of route numbers, filters the buses
 *  to return only the buses on the route numbers given (note that at certain
 *  times this may be more than one bus per route)
 */
function filterVehiclesByRoute(locations, routes) {

}

/** */
function magicMethodForBusThatHasChanged(bus) {
	return true;
}

setInterval(updateBusLocations, UPDATE_INTERVAL_MS);
