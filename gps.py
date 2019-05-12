#! /usr/bin/python
#https://github.com/MartijnBraam/gpsd-py3
import gpsd
import math
import time
import os
from datetime import datetime

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

#home="/home/pi/balloon/"
home="/home/felipe/Documents/radio/soft/globorasp/"
truncateDigits=4
#print("opening "+home+"gps.log")
initTime=datetime.utcnow()
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
			gps_pos=str(lat)+";"+str(lon)+";"+str(gpstime)+";"+str(alt)
			initTime=datetime.utcnow()
			formated_time = initTime.strftime("%Y%m%d_%H%M%S")
			data=formated_time+":"+gps_pos
			#print(data)
			f= open(home+"gps.log","a")
			f.write(data+"\n")
			f.close()
			time.sleep(10)

		except:
			#No GPS
			print("No GPS")
			print("0.0;0.0;;0.0")
	
except :
    print('End')

# See the inline docs for GpsResponse for the available data
#print(packet.position())
