#!/bin/bash

# Run the server. It must be run as root because we do direct memory mapping
# in order to drive the LEDs, which requires elevated privileges.
sudo pipenv run python app.py > server.log 2>&1 &
# or sudo pipenv run flask run [--host=0.0.0.0]

# Run the client
DISPLAY=:0 /usr/bin/chromium-browser --no-sandbox --noerrdialogs --disable-infobars --kiosk http://localhost:5000/
