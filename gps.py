#! /usr/bin/python
#https://github.com/MartijnBraam/gpsd-py3
import gpsd
import math
import time
import os

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper


truncateDigits=4


try:
	# Connect to the local gpsd
	gpsd.connect()
	while True:
		# Get gps position
		try:
			packet = gpsd.get_current()
			latitude=packet.lat
			lat=(truncate(latitude,truncateDigits))
			longitude=packet.lon
			lon=(truncate(longitude,truncateDigits))
			gpstime=packet.time
			altitude=packet.alt
			alt=(truncate(altitude,0))
			print(str(lat)+";"+str(lon)+";"+str(gpstime)+";"+str(alt))
			time.sleep(10)

		except:
			#No GPS
			print("No GPS")
			print("0.0;0.0;;0.0")
	
except :
    print('End')

# See the inline docs for GpsResponse for the available data
#print(packet.position())
