#!/bin/bash
# Russ Savela, russell.savela@snhu.edu, 2025
# 
# Configure instance with dependencies
#


sudo dnf -y install python3-pip git

pip3 install dash_leaflet dash pandas matplotlib boto3 bson


# git clone the code we are going to run
#  -it is public, so no keys needed 
#
#  This runs as the ec2-user, so it isn't root.  Still seems to set file permissions as root though

su -c "cd; git clone -b main https://github.com/russellsavela/cs499-enhancement-one.git" ec2-user

# Create a systemd service to run the app
#
 
cat << EOF > /etc/systemd/system/cs499-enhancement-one.service
[Unit]
Description=CS 499 - Enhancement Two Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /cs499-enhancement-one/enhancement.one.py

Restart=always
User=ec2-user
WorkingDirectory=/cs499-enhancement-one

[Install]
WantedBy=multi-user.target
EOF

# Run the app
#    better to do this as a system service, that will restart on failures

systemctl daemon-reload
systemctl enable cs499-enhancement-one.service
systemctl start cs499-enhancement-one.service
