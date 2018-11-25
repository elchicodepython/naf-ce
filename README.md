# NAF - CE

### Release 0.1

## Not Another Firewall

NAF-CE is a solution for adding or deleting iptables rules in order to allow or deny hosts based on DNS resolution.
NAF-CE is not a firewall and does'nt replace one. Is a custom solution for small teams of developers that wants to collaborate on a dedicated server without exposing it to everyone and without complex configurations.

NAF-CE check the domain resolution for each domain and add or delete the defined "allow_rule" rule replacing the {ip} keyword with the resolution of the domain name

## Requirements
python3
iptables

Tested on Ubuntu 18.04

## Installation
* git clone https://github.com/elchicodepython/naf-ce
* cd naf-ce
* sudo ./setup.sh
* sudo crontab -u root -e 
* Add the following line to crontab: 5 * * * * /usr/bin/naf-ce update

NAF-CE is based on a configuration file placed on /etc/naf/rules.json

Example of configuration file:

{
	"allow_rule": "-A INPUT -s {ip} ACCEPT",
	"domains": [
		{
		"name": "domain.com",
		"ip": "8.8.8.8"
		}
	]
}

## Add a domain

* Open /etc/naf/rules.json
* Add inside domains:[] a domain with the following structure: {"name": "mydomain.com", ip:""}
* It does'nt matter if we leave the IP empty at the moment
* Save the file

## Manual updating rules
* sudo naf-ce update




