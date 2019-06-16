# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
import datetime
import os
import math


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
message_tmp=gps_message.split(":")
gps_parts=message_tmp[1].split(";")
print(gps_parts)
lon=gps_parts[1]
lat=gps_parts[0]
hour=gps_parts[2]
alt=message_tmp[3].split(";")[1]
#print(alt_tmp)

callsign="EB2ELU-11"
outputfile="/tmp/aprs.wav"
time=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')
#speed="150" #m/s
#temp="-10" #grados centígrados
#alt="1000" #feet
msg="testing"
#pre="1000.0"

auxLat=float(lat)*100
auxLong=float(lon)*100
newLat=str(zpad(str(auxLat),4))
newLong=str(zpad(str(auxLong),4))

tmpLat=float(newLat)
tmpLong=float(newLong)

newLat=str(truncate(tmpLat,3))
newLong=str(truncate(tmpLong,3))

import os
try:
    os.remove(outputfile)
    print("File Removed!")
except:
    print("no file")

#http://wiki.ashab.space/doku.php?id=ns1:telemetria
#EA1IDZ-11>WORLD,WIDE2-2:!4331.52N/00540.05WO0/0.020/A=37.2/V=7.64/P=1018.0/TI=29.50/TO=26.94/23-04-2016/19:52:49/GPS=43.525415N,005.667503W/EA1IDZ test baliza APRS/SSTV ea1idz@ladecadence.net
message=callsign+">WORLD,WIDE2-2:!"+newLat+"N/"+newLong+"E/A="+alt+"/"+str(time[0])+"m/"+msg
print(message)
command="echo -n \""+message+"\" | gen_packets -a 100 -o "+outputfile+" - "
os.system(command)
#os.system("aplay "+outputfile)