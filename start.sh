#!/bin/bash
rm lock
python3 gps2.py &
./capture.sh &
python3 aprstx.py &

