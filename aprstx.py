# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon


#Indicativo
callsign="EB2ELU-11"
#Tiempo de espera en segundos para volver a mandar otra trama de APRS
waitTime=10
#Mensaje extra
msg="testing"



###############################################################
###############################################################
###############################################################
###############################################################
###NO TOCAR A PARTIR DE AQUI
###NO TOCAR A PARTIR DE AQUI
###NO TOCAR A PARTIR DE AQUI
###NO TOCAR A PARTIR DE AQUI
###NO TOCAR A PARTIR DE AQUI
###NO TOCAR A PARTIR DE AQUI
import datetime
import os
import math
import sys
import time
from pathlib import Path

home_folder="/home/pi/sstv/"
gps_file=home_folder+"gps.log"
outputfile=home_folder+"aprs.wav"
lastGPSLine="xxxxx"

#http://wiki.ashab.space/doku.php?id=ns1:telemetria
#EA1IDZ-11>WORLD,WIDE2-2:!4331.52N/00540.05WO0/0.020/A=37.2/V=7.64/P=1018.0/TI=29.50/TO=26.94/23-04-2016/19:52:49/GPS=43.525415N,005.667503W/EA1IDZ test baliza APRS/SSTV ea1idz@ladecadence.net


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



while True:
    time.sleep(waitTime)
    gps_message=getGPSLine(gps_file).rstrip()
    if "0.0;0.0;;0.0" in gps_message or lastGPSLine in gps_message:
        print("error or repeated")
        pass
    else:
        print(gps_message)
        lastGPSLine=gps_message
        message_tmp=gps_message.split(": ")
        gps_parts=message_tmp[1].split(";")
        lat=gps_parts[1].replace(" ","")
        latO=gps_parts[2].replace(" ","")
        lon=gps_parts[3].replace(" ","")
        lonO=gps_parts[4].replace(" ","")
        alt=gps_parts[5].replace(" ","")
        speed=gps_parts[6].replace(" ","")
        dateHour=gps_parts[0].replace(" ","")

        currentTime=datetime.datetime.utcnow().strftime("%H:%M:%S").split('.')


        newAlt=fill_with_leading_zeros(alt,6).split(".")[0]

        #try:
        #    os.remove(outputfile)
        #    #print("File Removed!")
        #except:
        #    print("no file")
            

        message=callsign+">WORLD,WIDE2-2:!"+lat[:-3]+latO+"/"+lon[:-3]+lonO+"O/"+speed+"/A="+newAlt+"/"+str(currentTime[0])+"/"+msg
        print(message)
        command="echo -n \""+message+"\" | gen_packets -a 100 -o "+outputfile+" - >/dev/null"
        os.system(command)
        while os.path.exists(home_folder+"/lock") is True:
            time.sleep(waitTime)
            pass
        Path(home_folder+"/lock").touch()
        #os.system("play -n synth 0:0:2 whitenoise")
        #os.system("aplay -f cdr "+outputfile)
        os.system("sudo -u pi aplay -f cdr "+outputfile)
        os.system("sudo -u pi aplay -f cdr "+outputfile)
        try:
            os.remove(home_folder+"/lock")
        except:
            print("no file")
