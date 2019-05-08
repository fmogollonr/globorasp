# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
# must be run as sudo
# Hay que ejecutar el script con sudo
import datetime
import os


def zpad(val, n):
    bits = val.split('.')
    if "-" in bits[0]:
        return "%s.%s" % (bits[0].zfill(n+1), bits[1])
    return "%s.%s" % (bits[0].zfill(n), bits[1])

callsign="EB2ELU"
outputfile="/tmp/aprs.wav"
time=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')
lat="43.3235"
lon="-1.9678"
speed="150" #m/s
temp="-10" #grados centígrados
alt="1000" #feet
msg="testing"

auxLat=float(lat)*100
auxLong=float(lon)*100
newLat=str(zpad(str(auxLat),6))
print(newLat)
newLong=str(zpad(str(auxLong),6))
print(newLong)

newLong=str(lon).ljust(2,'0')





#http://midnightcheese.com/2015/12/super-simple-aprs-position-beacon/
#$command = 'aprs -c '.$callsign.' -o packet.wav "/'.$time.'z'.$lat.'N/'.$lon.'W>'.$course.'/'.$speed.$comment.'/A='.$alt.'"';
#113851h4223.38N/00126.18WO036/007-I20-E-14-V6452mV Aranzadi Ikas. Katxiporreta II .3W&SSTV-A=082570
#192308h4738.18N/00858.74EO067/015/A=059062!wLc!Clb=-101.4m/s t=-52.4C Type=SRSC50 Wettersonden-Ballon radiosondy.info
command="aprs -c "+callsign+" -o "+outputfile+" \"/"+str(time[0])+"h"+newLat+"N/"+newLong+"E/A="+alt+"!Clb="+speed+"m/s t="+temp+"C "+msg+"\""
os.system(command)
#aprs -c $callsign -o $outputfile "$command"
os.system("aplay "+outputfile)