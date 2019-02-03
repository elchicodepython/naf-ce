#!/bin/bash

#
#	Basic iptables configuration for most use cases
#	handle it with care.
#
#	@elchicodepython
#


# Variables
IFACE="eth0"

# Flush previous rules
iptables -F
iptables -t nat -F

# Default DROP policy
iptables -P INPUT DROP
#iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Accept All Loopback traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Accept DNS querys
iptables -A INPUT -i $IFACE -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -o $IFACE -p udp --dport 53 -j ACCEPT

# Accept all stablished connections
# In order to allow NAF work with any TCP traffic
iptables -A INPUT -i $IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
