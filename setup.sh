#!/bin/bash

mkdir -p /opt/naf &&
mkdir -p /etc/naf && 
cp naf-ce.py /opt/naf &&
cp rules.json /opt/naf &&
chmod +x /opt/naf/naf-ce.py &&
ln -s /opt/naf/naf-ce.py /usr/bin/naf-ce &&
ln -s /opt/naf/rules.json /etc/naf/rules.json &&

echo "[ IPTABLES CONFIGURATION ]

Choose a configuration file inside of iptables/ folder or create one customized.
"

echo "Setup Done. Please add the following line to the crontab of a user with priviledges: 

5 * * * * /usr/bin/naf-ce update
"
