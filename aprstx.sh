#!/bin/sh 
# Este script transmite una trama aprs para hacer seguimiento de un globo aerostático
# This script will transmit an APRS trace to track a balloon
# must be run as sudo
# Hay que ejecutar el script con sudo

callsign="EB2ELU"
outputfile="aprs.wav"

aprs -c $callsign ":EMAIL    :test@example.com Test email" -o $outputfile

