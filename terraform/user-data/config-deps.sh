# Russ Savela, russell.savela@snhu.edu, 2025
# 
# Configure instance with dependencies
#

sudo dnf -y install python3-pip git

pip3 install dash_leaflet dash pandas matplotlib boto3


# git clone the code we are going to run
#  -it is public, so no keys needed

git clone https://github.com/russellsavela/cs499-enhancement-one.git
 
 
# Run the app
#

python3 cs499-enhancement-one/enhancement.one.py
