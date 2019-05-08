#! /usr/bin/python
#https://github.com/MartijnBraam/gpsd-py3
import gpsd
import math

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

truncateDigits=4
# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
gpsd.connect(host="127.0.0.1", port=2947)

# Get gps position
try:
	packet = gpsd.get_current()
	latitude=packet.lat
	lat=(truncate(latitude,truncateDigits))
	longitude=packet.lon
	lon=(truncate(longitude,truncateDigits))
	time=packet.time
	altitude=packet.alt
	alt=(truncate(altitude,0))
	print(str(lat)+";"+str(lon)+";"+str(time)+";"+str(alt))

except:
	#No GPS
	print("0.0;0.0;;0.0")

# See the inline docs for GpsResponse for the available data
#print(packet.position())
