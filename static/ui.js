function updateClock() {
    document.getElementById('clock').innerHTML = new Date().toLocaleTimeString();
}

async function updateRoutes() {
    // NONE OF THIS WORKS. We're confusing buses with upcoming stop times. Out of scope?
    let res = await fetch('/api/get-upcoming-departures');
    let buses = await res.json();
    for (let bus of buses) {
        let bus_info_div;
        for (let el of document.getElementsByClassName("bus-id")) {
            if (el.innerHTML == bus.route) {
                bus_div = el.parentElement.getElementsByClassName("bus-info")[0];
            }
        }
        bus_info_div.innerHTML = `to_downtown: ${"6:34 PM"} (${"2m late"})<br>from_downtown: ${"6:38 PM"} (${"on time"})`
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
