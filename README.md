# NAF - CE



## Not Another Firewall

NAF-CE is a solution for adding or deleting iptables rules in order to allow or deny hosts based on DNS resolution.
NAF-CE is not a firewall and doesn't replace one. Its a custom solution for small teams of developers that wants to collaborate on a dedicated server without exposing it to everyone and without having to deal with complex configurations.

NAF-CE check the domain resolution for each domain and add or delete the defined "allow_rule" rule replacing the {ip} keyword with the resolution of the domain name

It should be use with a dynamic DNS provider such as DuckDNS.

Steps after installation:
* Set a dynamic DNS for a domain name in a third party platform
* Set that domain in NAF-CE configuration
* NAF will update the IPTables defined rule (by default accepting the ip of that domain inside de INPUT chain) each time the domain resolution change.
* If everything is correct set a default drop policy inside iptables for incomming packets.
* NAF-CE will act as a whitelist allowing only (by default) the IPs resolved by the dynamic DNS provider to the domain names specified in configuration.

## Requirements
- python3
- iptables

### Tested on
- Ubuntu 18.04
- Proxmox PVE 5

## Installation
* git clone https://github.com/elchicodepython/naf-ce
* cd naf-ce
* sudo ./setup.sh
* sudo crontab -u root -e 
* Add the following line to crontab: 5 * * * * /usr/bin/naf-ce update

### Interactive configuration

TODO: To be completed

## Manual Configuration

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

### Add a domain

* Open /etc/naf/rules.json
* Add inside domains:[] a domain with the following structure: {"name": "mydomain.com", ip:""}
* It doesn't matter if we leave the IP empty at the moment
* Save the file

### Manual updating rules
* sudo naf-ce update




