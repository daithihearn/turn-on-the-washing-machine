#!/bin/bash
export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x16 &
XVFB_PID=$!
sleep 5

for job in "$@"
do
    /usr/bin/python3 $job
done 

kill $XVFB_PID