#!/bin/bash

# Run the server
pipenv run python server.py > server.log 2>&1 &

# Run the client
DISPLAY=:0 /usr/bin/chromium-browser --no-sandbox --noerrdialogs --disable-infobars --kiosk http://localhost:5000/
