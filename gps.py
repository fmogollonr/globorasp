#! /usr/bin/python
#https://github.com/MartijnBraam/gpsd-py3
import gpsd

# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
gpsd.connect(host="127.0.0.1", port=2947)

# Get gps position
packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data
#print(packet.position())
print(str(packet.lat)+";"+str(packet.lon)+";"+str(packet.time)+";"+str(packet.alt))
