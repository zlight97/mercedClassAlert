#!/bin/bash
if [ ! -d ~/BobcatLogs/ ]; then
    echo making Logs dir
    mkdir -p ~/BobcatLogs/;
    echo Logs creaed
fi
filename=$(date +%m.%d.%Y,%H:%M:%S.log)
echo creating file ~/BobcatLogs/$filename
touch ~/BobcatLogs/$filename
echo Lauching classAlert.py
python -u classAlert.py | tee -a ~/BobcatLogs/$filename