import time
import json
import smbus
import logging 
import math
import os
from datetime import datetime

BUS = None
address = 0x42
gpsReadInterval = 0.1
LOG = logging.getLogger()
truncateDigits=4
home="/home/pi/sstv/"
initTime=datetime.utcnow()
gpsdateString=""

# GUIDE
# http://ava.upuaut.net/?p=768

GPSDAT = {
    'strType': None,
    'fixTime': None,
    'lat': None,
    'latDir': None,
    'lon': None,
    'lonDir': None,
    'fixQual': None,
    'numSat': None,
    'horDil': None,
    'alt': None,
    'altUnit': None,
    'galt': None,
    'galtUnit': None,
    'DPGS_updt': None,
    'DPGS_ID': None
}

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def connectBus():
    global BUS
    BUS = smbus.SMBus(1)

def parseResponse(gpsLine):

    global lastLocation
    gpsChars = ''.join(chr(c) for c in gpsLine)
    if "*" not in gpsChars:
        return False

    gpsStr, chkSum = gpsChars.split('*')  
    #print(gpsStr)  
    gpsComponents = gpsStr.split(',')
    gpsStart = gpsComponents[0]
    if (gpsStart == "$GNRMC"):
        global gpsdate
        gpsdateString =json.dumps(gpsComponents[9]).replace('"','')
        print("date is "+gpsdateString)
    elif (gpsStart == "$GNGGA"):
        chkVal = 0
        for ch in gpsStr[1:]: # Remove the $
            chkVal ^= ord(ch)
        if (chkVal == int(chkSum, 16)):
            for i, k in enumerate(
                ['strType', 'fixTime', 
                'lat', 'latDir', 'lon', 'lonDir',
                'fixQual', 'numSat', 'horDil', 
                'alt', 'altUnit', 'galt', 'galtUnit',
                'DPGS_updt', 'DPGS_ID']):
                GPSDAT[k] = gpsComponents[i]
            latitude=float(json.dumps(GPSDAT['lat']).replace('"',''))/100
            longitude=float(json.dumps(GPSDAT['lon']).replace('"',''))/100
            altitude=float(json.dumps(GPSDAT['alt']).replace('"',''))
            #time=json.dumps(GPSDAT['fixTime']).replace('"','')
            #gpstime = datetime.strptime(gpsdate+" "+str(time), '%d%m%Y%m %H%M%S.%f')
            #lon=truncate(longitude,truncateDigits)
            #lat=truncate(latitude,truncateDigits)
            #alt=(truncate(altitude,0))

            #gps_pos=str(lat)+";"+str(lon)+";"+str(gpstime)+";"+str(alt)
            #initTime=datetime.utcnow()
            #formated_time = initTime.strftime("%Y%m%d_%H%M%S")
            #data=formated_time+": "+gps_pos
            #f= open(home+"gps.log","a")
            #f.write(data+"\n")
            #f.close()
            time.sleep(10)

def readGPS():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            c = BUS.read_byte(address)
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
        parseResponse(response)
    except IOError:
        time.sleep(0.5)
        connectBus()
    except Exception as e:
        print(e)
    #    LOG.error(e)

connectBus()
while True:
    readGPS()
    time.sleep(gpsReadInterval)
