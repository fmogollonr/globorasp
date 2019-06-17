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
timeout=1
gpserror=0

print("startgps")

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


def split_number(s,number):
    return [s[i:i+number] for i in range(0, len(s), number)]

def string_date_to_date(dateString,time):
    splittedDate=split_number(dateString,2)
    year="20"+splittedDate[2]
    month=splittedDate[1]
    day=splittedDate[0]
    splittedTime=split_number(time,2)
    hour=splittedTime[0]
    minute=splittedTime[1]
    secs=splittedTime[2]
    if year.isdigit() and month.isdigit() and day.isdigit() and hour.isdigit() and minute.isdigit() and secs.isdigit():
        dateTime=datetime(int(year),int(month),int(day),int(hour),int(minute),int(secs))
        return dateTime


def connectBus():
    global BUS
    BUS = smbus.SMBus(1)

def parseResponse(gpsLine):
    gpsChars = ''.join(chr(c) for c in gpsLine)
    if "*" not in gpsChars:
        return False

    gpsStr, chkSum = gpsChars.split('*')  
    #print(gpsStr)  
    gpsComponents = gpsStr.split(',')
    gpsStart = gpsComponents[0]
    if (gpsStart == "$GNRMC"):
        global gpsdateString
        gpsdateString =json.dumps(gpsComponents[9]).replace('"','')
    elif (gpsStart == "$GPRMC"):
        print("GPRMC")
        print(gpsComponents)
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
            if (GPSDAT['lat']) is '' or GPSDAT['lon'] is '' or GPSDAT['alt'] is '':
                gps_error()
            else:
                #print("gps position")
                #print(GPSDAT['lat'])
                #print(GPSDAT['lon'])
                global gpserror
                gpserror=0

                altitude=float(json.dumps(GPSDAT['alt']).replace('"',''))
                gpstime=json.dumps(GPSDAT['fixTime']).replace('"','')
                truncatedTime=gpstime.split(".")[0]
                alt=float((truncate(altitude,0))*3.28084)
                newdate=string_date_to_date(gpsdateString,truncatedTime)
                if newdate is not -1:
                    printdate=newdate.strftime("%Y-%m-%dT%H:%M:%S.00Z")
                    presdate=newdate.strftime("%Y%m%d_%H%M%S")
                    #gps_pos=str(presdate)+": "+str(lat)+";"+GPSDAT['latDir']+";"+str(lon)+";"+GPSDAT['lonDir']+";"+printdate+";"+str(alt)
                    gps_pos=str(presdate)+": "+GPSDAT['lat']+";"+GPSDAT['latDir']+";"+GPSDAT['lon']+";"+GPSDAT['lonDir']+";"+printdate+";"+str(alt)
                    print(gps_pos)
                    f= open(home+"gps.log","a")
                    f.write(gps_pos+"\n")
                    f.close()
                    time.sleep(timeout)

def gps_error():
    global gpserror
    gpserror+=1
    #print("gpserror"+str(gpserror))
    if gpserror== 10:
        gpserror=0
        print("No GPS")
        print("0.0;0.0;;0.0")
        initTime=datetime.utcnow()
        formated_time = initTime.strftime("%Y%m%d_%H%M%S")
        gps_pos="0.0;0.0;;0.0"
        data=formated_time+": "+gps_pos
        f= open(home+"gps.log","a")
        f.write(data+"\n")
        f.close()
        time.sleep(timeout)

def readGPS():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            try:
                c = BUS.read_byte(address)
                if c == 255:
                    return False
                elif c == 10:
                    break
                else:
                    response.append(c)
            except Exception as e:
                print(e)
                gps_error()
        parseResponse(response)
    except IOError:
        print("IO error")
        time.sleep(0.5)
        connectBus()
    except Exception as e:
        print(e)
        gps_error()
    #    LOG.error(e)

connectBus()
while True:
    readGPS()
    time.sleep(gpsReadInterval)
