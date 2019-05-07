#!/bin/sh 
# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
# must be run as sudo
# Hay que ejecutar el script con sudo

callsign="EB2ELU"
outputfile="aprs.wav"
time=`date +"%Y-%m-%d %T" --utc`
lat="45.26"
lon="10.1"
speed="150"
temp="-10"
alt="1000"

#http://midnightcheese.com/2015/12/super-simple-aprs-position-beacon/
#$command = 'aprs -c '.$callsign.' -o packet.wav "/'.$time.'z'.$lat.'N/'.$lon.'W>'.$course.'/'.$speed.$comment.'/A='.$alt.'"';
command="/$time""z""$lat""N""$lon""W/$speed/A=$alt"
aprs -c $callsign -o $outputfile "$command"

