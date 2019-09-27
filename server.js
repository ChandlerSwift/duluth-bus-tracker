const ws = require('ws');
const fetch = require('node-fetch');

const UPDATE_INTERVAL_MS = 5000;
const VEHICLE_POSITION_DATA_URL = 'http://duluthtransit.com/TMGTFSRealTimeWebService/Vehicle/VehiclePositions.json';
const wss = new ws.Server({ port: 8080 });

let connections = [];

wss.on('connection', function connection(conn) {
	conn.on('message', function incoming(message) {
		// discard messages (for now?)
	});

	connections.push(conn);
});

let buses = [];

/** Checks for updated bus locations, and sends updates to all connected clients */
async function updateBusLocations() {
	const vehicles = await getVehicles();
	const relevantVehicles = filterVehiclesByRoute(vehicles, ['6', '13', '23']);
	for (let bus of relevantVehicles) {
		console.log(`Sending update for bus ${bus}`);
		for (let conn of connections) {
			const update = '' // TODO
			conn.send(update);
		}
	}
}

/** Downloads the location of all buses, returns as an array of buses */
async function getVehicles() {
	const response = await fetch(VEHICLE_POSITION_DATA_URL);
	const vehicle_data = await response.json();
	return vehicle_data.entity;
}

/** Given an array of buses and an array of route numbers, filters the buses
 *  to return only the buses on the route numbers given (note that at certain
 *  times this may be more than one bus per route)
 */
function filterVehiclesByRoute(vehicles, routes) {
	return vehicles.filter(vehicle => routes.includes(vehicle.vehicle.trip.route_id));
}

setInterval(updateBusLocations, UPDATE_INTERVAL_MS);
