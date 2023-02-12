#!/bin/bash

pip3 install -r requirements.txt

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH

sudo rm -f /lib/systemd/system/rhasspy.skill.advtimer.service
touch /lib/systemd/system/rhasspy.skill.advtimer.service
:> /lib/systemd/system/rhasspy.skill.advtimer.service

echo "
[Unit]
Description=Rhasspy Advanced Timer Skill
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPTPATH/hermes-app-advtimer.py
Restart=on-abort

[Install]
WantedBy=multi-user.target

  " >>  /lib/systemd/system/rhasspy.skill.advtimer.service


chmod +x hermes-app-advtimer.py


sudo sudo chmod 644 /lib/systemd/system/rhasspy.skill.advtimer.service
sudo systemctl stop rhasspy.skill.advtimer.service
sudo systemctl daemon-reload
sudo systemctl enable rhasspy.skill.advtimer.service
sudo systemctl start rhasspy.skill.advtimer.service
#sudo reboot