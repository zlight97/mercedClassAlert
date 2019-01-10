#!/bin/bash
if [ ! -d Logs ]; then
    echo making Logs dir
    mkdir -p Logs;
    echo Logs creaed
fi
filename=$(date +'Logs/%m.%d.%Y,%H:%M:%S.log')
echo Lauching classAlert.py
python -u classAlert.py | tee $filename
