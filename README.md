# Duluth Bus Tracker 
### (For Keeping Track of Buses in Duluth)

Backend for the sign that is going to display where the buses are in Duluth!

Raspberry pi display uses ui.html to display information on bus times

[DTA bus API info](https://www.duluthtransit.com/home/doing-business/developer-resources/)

### Installation Notes
When installing, the lights are driven over PWM on GPIO12. This normally
requires root access to read/write `/dev/mem`. Instead, since it's difficult
to run some of the other components as root, we allow the user (`pi` in this
case) to write to `/dev/mem` by `chmod g+w /dev/mem; usermod -aG kmem pi`.

We also need `python3`, `pip(3)`, and `pipenv`:
```
sudo apt install python3 python3-pip
pip3 install pipenv
export PATH=$PATH:$HOME/.local/bin
sudo pipenv install # since we're running the pipenv as root, we need to install it as root
```

You'll need to set up the routes you want. For that, we provide the file
`util/generate_routes.sh`, which can be run more-or-less as-is. If you want
different routes than the routes I use (6, 11, 11K, 13, 23), then you'll need
to edit those values at a few points in the file. Then, run the script. It'll
download the latest data from Duluth Transit's website, run it through a whole
pile of different scripts in different languages (SQL to deal with highly
relational data, Python to deal with more complex list manipulation and export,
and a whole bunch of bash to easily tie it all together), prompt you for a bit
of data, and eventually drop a bunch of json which you can save as routes.json
in the `map_updater` directory!

Once you're done setting up the server, you can either simply run the startup
script, `./startup.sh`, which will launch both the server and a Chromium
instance to run the display, or run it yourself with two `tmux` windows. I
personally tend to prefer the `tmux` method since it allows me to view the
output of both, though the startup script does output logs to a file. It also
allows me to individually start/stop/restart the services, which is helpful
during development.
