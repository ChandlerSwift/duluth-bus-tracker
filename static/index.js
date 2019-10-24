setInterval(updateClock, 100);
setInterval(updateRoutes, 5000);

function updateClock() {
    document.getElementById('clock').innerHTML = new Date().toLocaleTimeString();
}

async function updateRoutes() {
    let res = await fetch('/api/get-buses');
    let bus_info = await res.json();
    console.log(bus_info);
}

// Select current routes
let is_route_currently_selected = false;

for (let route_div of document.getElementsByClassName('route')) {
    route_div.onclick = function(e) {
        if (is_route_currently_selected) {
            for (let route_div of document.getElementsByClassName('route')) {
                route_div.style.opacity = 1.0;
            }
        } else { // select the route
            for (let other_route_div of document.getElementsByClassName('route')) {
                if (route_div == other_route_div)
                    continue;
                other_route_div.style.opacity = 0.1;
            }
        }
        is_route_currently_selected = !is_route_currently_selected;
    }
}
