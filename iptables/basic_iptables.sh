#!/bin/bash

#
#	Basic iptables configuration for most use cases
#	handle it with care.
#
#	@elchicodepython
#

iptables -F
iptables -t nat -F
iptables -P INPUT DROP
iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
