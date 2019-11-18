function updateClock() {
    document.getElementById('clock').innerHTML = new Date().toLocaleTimeString();
}

async function updateRoutes() {
    let res = await fetch('/api/get-upcoming-departures');
    let buses = await res.json();
    for (let info_div of document.getElementsByClassName('bus-info')) {
        info_div.innerHTML = "";
    }
    for (let bus of buses) {
        let info_div = document.getElementById(`bus-info-${bus.route}`)
        let departure_time = new Date(bus.time * 1000); // milliseconds after epoch
        let departure_time_string = departure_time.toLocaleTimeString(); // TODO: remove seconds
        info_div.innerHTML += `${bus.direction}: ${departure_time_string}<br>`;
    }
    for (let info_div of document.getElementsByClassName('bus-info')) {
        if (info_div.innerHTML == "") {
            info_div.innerHTML = "No upcoming departures.";
        }
    }
}

// Select current routes
let is_route_currently_selected = false;

for (let route_div of document.getElementsByClassName('route')) {
    route_div.onclick = function(e) {
        if (is_route_currently_selected) {
            fetch('/api/show-all-routes');
            for (let route_div of document.getElementsByClassName('route')) {
                route_div.style.opacity = 1.0;
            }
        } else { // select the route
            fetch('/api/show-route/' + route_div.dataset['route']);
            for (let other_route_div of document.getElementsByClassName('route')) {
                if (route_div == other_route_div)
                    continue;
                other_route_div.style.opacity = 0.1;
            }
        }
        is_route_currently_selected = !is_route_currently_selected;
    }
}
