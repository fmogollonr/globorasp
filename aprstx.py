# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
import datetime
import os


def zpad(val, n):
    bits = val.split('.')
    if "-" in bits[0]:
        return "%s.%s" % (bits[0].zfill(n+1), bits[1])
    return "%s.%s" % (bits[0].zfill(n), bits[1])


callsign="EB2ELU-11"
outputfile="/tmp/aprs.wav"
time=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')
lat="43.3235"
lon="-1.9678"
speed="150" #m/s
temp="-10" #grados centígrados
alt="1000" #feet
msg="testing"
pre="1000.0"

auxLat=float(lat)*100
auxLong=float(lon)*100
newLat=str(zpad(str(auxLat),6))
newLong=str(zpad(str(auxLong),6))

import os
try:
    os.remove(outputfile)
    print("File Removed!")
except:
    print("no file")

#http://wiki.ashab.space/doku.php?id=ns1:telemetria
#EA1IDZ-11>WORLD,WIDE2-2:!4331.52N/00540.05WO0/0.020/A=37.2/V=7.64/P=1018.0/TI=29.50/TO=26.94/23-04-2016/19:52:49/GPS=43.525415N,005.667503W/EA1IDZ test baliza APRS/SSTV ea1idz@ladecadence.net
message=callsign+">WORLD,WIDE2-2:!"+newLat+"N/"+newLong+"E/"+speed+"/A="+alt+"/TO="+temp+"/"+str(time[0])+"/"+msg
command="echo -n \""+message+"\" | gen_packets -a 100 -o "+outputfile+" - "
os.system(command)
os.system("aplay "+outputfile)