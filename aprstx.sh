#!/bin/sh 
# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
# must be run as sudo
# Hay que ejecutar el script con sudo

callsign="EB2ELU"
outputfile="aprs.wav"
time=`date +"%H%M%S" --utc`
lat="4332.35"
lon="-0196.78"
speed="150" #m/s
temp="-10" #grados centígrados
alt="1000" #feet
msg="testing "

#http://midnightcheese.com/2015/12/super-simple-aprs-position-beacon/
#$command = 'aprs -c '.$callsign.' -o packet.wav "/'.$time.'z'.$lat.'N/'.$lon.'W>'.$course.'/'.$speed.$comment.'/A='.$alt.'"';
#113851h4223.38N/00126.18WO036/007-I20-E-14-V6452mV Aranzadi Ikas. Katxiporreta II .3W&SSTV-A=082570
#192308h4738.18N/00858.74EO067/015/A=059062!wLc!Clb=-101.4m/s t=-52.4C Type=SRSC50 Wettersonden-Ballon radiosondy.info
command="/$time""h""$lat""N/""$lon""E/A=$alt!Clb="$speed"m/s t="$temp"C "$msg
echo $command
aprs -c $callsign -o $outputfile "$command"
aplay $outputfile

