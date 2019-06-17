# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
import datetime
import os
import math
import sys

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def fill_with_leading_zeros(val, n):
    bits = val.split('.')
    if "-" in bits[0]:
        return "%s.%s" % (bits[0].zfill(n+1), bits[1])
    return "%s.%s" % (bits[0].zfill(n), bits[1])

def split_number(s,number):
    return [s[i:i+number] for i in range(0, len(s), number)]

def string_to_ggmmss(pos):
    tmp=pos.replace(" ","").split(".")
    gra=tmp[0]
    mmss=tmp[1]
    tmp=split_number(mmss,2)
    minutes=tmp[0]
    secs=tmp[1]
    return gra,minutes,secs

def getGPSLine(filePath):
    fileHandle = open ( filePath,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    return lineList[-1]

home_folder="/home/pi/sstv/"
gps_file=home_folder+"gps.log"
gps_message=getGPSLine(gps_file).rstrip()
print(gps_message)
if "0.0;0.0;;0.0" in gps_message:
    print("error")
    sys.exit()
message_tmp=gps_message.split(":")
gps_parts=message_tmp[1].split(";")
lat=gps_parts[0].replace(" ","")
latO=gps_parts[1].replace(" ","")
lon=gps_parts[2].replace(" ","")
lonO=gps_parts[3].replace(" ","")
hour=gps_parts[4].replace(" ","")
alt=message_tmp[3].split(";")[1].replace(" ","")

callsign="EB2ELU-11"
time=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')
#speed="150" #m/s
#temp="-10" #grados centígrados
#alt="1000" #feet
msg="testing"




latGra,latMin,latSecs=string_to_ggmmss(lat)

print("latitude "+latGra+" : "+latMin+" : "+latSecs)
lonGra,lonMin,lonSecs=string_to_ggmmss(lon)
print("longitude "+lonGra+" : "+lonMin+" : "+lonSecs)

newLat=fill_with_leading_zeros(latGra+latMin+"."+latSecs,4)
newLong=fill_with_leading_zeros(lonGra+lonMin+"."+lonSecs,5)
newAlt=fill_with_leading_zeros(alt,6).split(".")[0]


#print("newLat "+newLat)
#print("newLong "+newLong)



import os
try:
    os.remove(outputfile)
    print("File Removed!")
except:
    print("no file")

#http://wiki.ashab.space/doku.php?id=ns1:telemetria
#EA1IDZ-11>WORLD,WIDE2-2:!4331.52N/00540.05WO0/0.020/A=37.2/V=7.64/P=1018.0/TI=29.50/TO=26.94/23-04-2016/19:52:49/GPS=43.525415N,005.667503W/EA1IDZ test baliza APRS/SSTV ea1idz@ladecadence.net
message=callsign+">WORLD,WIDE2-2:!"+lat[:-3]+latO+"/"+lon[:-3]+lonO+"O/A="+newAlt+"/"+str(time[0])+"/"+msg
print(message)
command="echo -n \""+message+"\" | gen_packets -a 100 -o "+home_folder+"aprs.wav - "
os.system(command)
#os.system("aplay "+outputfile)