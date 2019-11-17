#!/bin/bash

# Run the server. It must be run as root because we do direct memory mapping
# in order to drive the LEDs, which requires elevated privileges.
sudo pipenv run python server.py > server.log 2>&1 &

# Run the client
DISPLAY=:0 /usr/bin/chromium-browser --no-sandbox --noerrdialogs --disable-infobars --kiosk http://localhost:5000/
