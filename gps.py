#! /usr/bin/python
#https://github.com/MartijnBraam/gpsd-py3
import gpsd

# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
gpsd.connect(host="127.0.0.1", port=2947)

# Get gps position
try:
	packet = gpsd.get_current()
	print(str(packet.lat)+";"+str(packet.lon)+";"+str(packet.time)+";"+str(packet.alt))
except:
	#No GPS
	print("0.0;0.0;;0.0")

# See the inline docs for GpsResponse for the available data
#print(packet.position())
