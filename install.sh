#!/bin/sh 
sudo apt-get update
sudo apt-get install python-pyaudio python3-pyaudio imagemagick direwolf -y
sudo pip3 install pySSTV gpsd-py3
echo '# Default settings for the gpsd init script and the hotplug wrapper.
# Start the gpsd daemon automatically at boot time
START_DAEMON="false"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="true"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyUSB0"

# Other options you want to pass to gpsd
GPSD_OPTIONS="-n -G -b"
GPSD_SOCKET="/var/run/gpsd.sock"
#end of file gpsda' > /etc/default/gpsd
