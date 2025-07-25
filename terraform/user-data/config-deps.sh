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
#  This runs as the ec2-user, so it isn't root.

su -c "cd; git clone https://github.com/russellsavela/cs499-enhancement-one.git" ec2-user

# Create a systemd service to run the app
#
 
cat << EOF > /etc/systemd/system/cs499-enhancement-one.service
[Unit]
Description=Your Server Process
After=network.target

[Service]
ExecStart=/cs499-enhancement-one/enhancement.one.py

Restart=always
User=ec2-user
WorkingDirectory=/home/ec2-user/cs499-enhancement-one

[Install]
WantedBy=multi-user.target
EOF

# Run the app
#

systemctl enable cs499-enhancement-one.service
systemctl start cs499-enhancement-one.service

#su -c "cd; python3 cs499-enhancement-one/enhancement.one.py" ec2-user
