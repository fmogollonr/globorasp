# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
import datetime
import os
import math
import sys


def dd2dms(longitude, latitude):

    # math.modf() splits whole number and decimal into tuple
    # eg 53.3478 becomes (0.3478, 53)
    split_degx = math.modf(longitude)
    
    # the whole number [index 1] is the degrees
    degrees_x = int(split_degx[1])

    # multiply the decimal part by 60: 0.3478 * 60 = 20.868
    # split the whole number part of the total as the minutes: 20
    # abs() absoulte value - no negative
    minutes_x = abs(int(math.modf(split_degx[0] * 60)[1]))

    # multiply the decimal part of the split above by 60 to get the seconds
    # 0.868 x 60 = 52.08, round excess decimal places to 2 places
    # abs() absoulte value - no negative
    seconds_x = abs(round(math.modf(split_degx[0] * 60)[0] * 60,2))

    # repeat for latitude
    split_degy = math.modf(latitude)
    degrees_y = int(split_degy[1])
    minutes_y = abs(int(math.modf(split_degy[0] * 60)[1]))
    seconds_y = abs(round(math.modf(split_degy[0] * 60)[0] * 60,2))

    # account for E/W & N/S
    if degrees_x < 0:
        EorW = "W"
    else:
        EorW = "E"

    if degrees_y < 0:
        NorS = "S"
    else:
        NorS = "N"
    
    lat=str(abs(degrees_x))+str(minutes_x)+str(seconds_x)
    lon=str(abs(degrees_y))+str(minutes_y)+str(seconds_y)

    # abs() remove negative from degrees, was only needed for if-else above
    #print("\t" + str(abs(degrees_x)) + u"\u00b0 " + str(minutes_x) + "' " + str(seconds_x) + "\" " + EorW)
    #print("\t" + str(abs(degrees_y)) + u"\u00b0 " + str(minutes_y) + "' " + str(seconds_y) + "\" " + NorS)
    
    return lat,lon

def zpad(val, n):
    bits = val.split('.')
    if "-" in bits[0]:
        return "%s.%s" % (bits[0].zfill(n+1), bits[1])
    return "%s.%s" % (bits[0].zfill(n), bits[1])


def getGPSLine(filePath):
    fileHandle = open ( filePath,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    #print("The last line is:")
    # or simply
    #print(lineList[-1])
    return lineList[-1]

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

home_folder="/home/pi/sstv/"
gps_file=home_folder+"gps.log"
gps_message=getGPSLine(gps_file).rstrip()
print(gps_message)
if "0.0;0.0;;0.0" in gps_message:
    print("error")
    sys.exit()
message_tmp=gps_message.split(":")
gps_parts=message_tmp[1].split(";")
lon=gps_parts[1]
lat=gps_parts[0]
hour=gps_parts[2]
alt=message_tmp[3].split(";")[1]
#print(alt_tmp)

callsign="EB2ELU-11"
#outputfile="/tmp/aprs.wav"
time=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')
#speed="150" #m/s
#temp="-10" #grados centígrados
#alt="1000" #feet
msg="testing"
#pre="1000.0"
speed="0.020"

print("lat "+lat)
print("lat "+lat)

auxLat=float(lat)
auxLong=float(lon)

lon,lat=dd2dms(auxLong,auxLat)
print(lon)
print(lat)

latitude=float(lat)/100
longitude=float(lon)/100

newLat=str(zpad(str(latitude),4))
newLong=str(zpad(str(longitude),4))

tmpLat=float(newLat)
tmpLong=float(newLong)

newLat=zpad(str(truncate(tmpLat,2)),4)
newLong=zpad(str(truncate(tmpLong,2)),5)


import os
try:
    os.remove(outputfile)
    print("File Removed!")
except:
    print("no file")

#http://wiki.ashab.space/doku.php?id=ns1:telemetria
#EA1IDZ-11>WORLD,WIDE2-2:!4331.52N/00540.05WO0/0.020/A=37.2/V=7.64/P=1018.0/TI=29.50/TO=26.94/23-04-2016/19:52:49/GPS=43.525415N,005.667503W/EA1IDZ test baliza APRS/SSTV ea1idz@ladecadence.net
message=callsign+">WORLD,WIDE2-2:!"+newLat+"N/"+newLong+"W/0"+speed+"/A="+alt+"/"+str(time[0])+"/"+msg
print(message)
command="echo -n \""+message+"\" | gen_packets -a 100 -o "+home_folder+"aprs.wav - "
os.system(command)
#os.system("aplay "+outputfile)