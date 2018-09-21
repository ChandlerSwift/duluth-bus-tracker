wget -q http://www.duluthtransit.com/gtf/google_transit.zip
rm -r data
mkdir data
unzip -qd data google_transit.zip
rm google_transit.zip
echo "Files downloaded to $(echo data/*)"
