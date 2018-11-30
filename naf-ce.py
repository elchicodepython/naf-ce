#!/usr/bin/env python3
import socket, json, subprocess, os.path, sys
from functools import wraps


RULES_FILE = '/etc/naf/rules.json'
DEFAULT_ALLOW_RULE = "-P INPUT -s {ip}/32 ACCEPT"


'''
Rules is a python dictionary with the following structure:

{
	"allow_rule": "-P INPUT -src {ip} ACCEPT",
	"domains": [
		{
		"name": "domain.com",
		"ip": "8.8.8.8"
		}
	]
}

Copyright Samuel López Saura 2018
Linkedin https://www.linkedin.com/in/sam-sec
'''

print(r'''
 _   _    _    _____ 
| \ | |  / \  |  ___|
|  \| | / _ \ | |_   
| |\  |/ ___ \|  _|  
|_| \_/_/   \_\_|     
                  
Not Another Firewall - CE

	Release 0.1
    @elchicodepython

''')

def issafe(rule):
	if '&' in rule or ';' in rule:
		return False
	return True

def list_iptables():
	data = subprocess.check_output('iptables -S', shell=True).decode()
	return data.split('\n')

def delete_iptables_rule(rule):
	subprocess.check_output('iptables -D %s' % rule.replace('-A', ''), shell=True)

def add_iptables_rule(rule):
	subprocess.check_output('iptables %s' % rule, shell=True)

def get_rules():
	with open(RULES_FILE, 'r') as file:
		rules = json.loads(file.read())
	return rules

def save_rules(rules):
	with open(RULES_FILE, 'w') as file:
		file.write(json.dumps(rules))

def check_domains():

	rules = get_rules()

	current_iptables = list_iptables()
	allow_rule = rules.get('allow_rule', DEFAULT_ALLOW_RULE)

	for domain in rules.get('domains', []):
		domain_name =  domain.get('name', None)
		if domain_name:	
			print(('Checking %s' % domain_name).format(80, '='))
			ip_data = domain.get('ip')

			try:
				real_ip = socket.gethostbyname(domain_name)
			except socket.gaierror:
				print('Error on name resolution for %s' % domain_name)
				continue

			if issafe(real_ip):
				print('IP FOUND %s' % real_ip)
				rule_ip_data = allow_rule.format(ip = ip_data)
				rule_real_ip = allow_rule.format(ip = real_ip)

				if (rule_ip_data != rule_real_ip):
					print('IP saved [%s] != real ip [%s]' % (ip_data, real_ip))
					if rule_ip_data in current_iptables:
						delete_iptables_rule(rule_ip_data)
						print('[%s] Deleted from iptables' % ip_data)
					if rule_real_ip not in current_iptables:
						add_iptables_rule(rule_real_ip)
						print('[%s] Added to iptables' % real_ip)
				else:
					print('Without changes')

				domain['ip'] = real_ip

	save_rules(rules)




def edit_rules():
	action = ''

	print('''Choose an option
1) Add a domain
2) Delete a domain
3) List configuration
4) Update rules
x) Exit''')

	while action != 'x':
		action = input('> ')
		if action == '1':
			edit_rules_add_domain()
		elif action == '2':
			edit_rules_delete_domain()
		elif action == '3':
			list_rules()
		elif action == '4':
			check_domains()
		elif action == 'x':
			return

def rules_context(f):
	@wraps(f)
	def foo(*args, **kwargs):
		rules = get_rules()
		o = f(rules, *args, **kwargs)
		save_rules(rules)
		return o
	return foo

@rules_context
def edit_rules_add_domain(rules):
	dom = input('[\033[1;32ma\033[0m] Domain: ')
	rules['domains'].append({'name': dom, 'ip': ''})


@rules_context
def edit_rules_delete_domain(rules):
	founded = False
	dom = input('[\033[1;31md\033[0m] Domain: ')
	for idx, domain in enumerate(rules['domains']):
		if domain['name'] == dom:
			founded = True
			break
	if founded:
		print('[200] Deleted')
		del rules['domains'][idx]
	else:
		print('[404] Not Found')

def list_rules():
	rules = get_rules()
	print('\033[1;32mALLOW RULE: %s\033[0m' % rules.get('allow_rule', DEFAULT_ALLOW_RULE))
	print('Domains:')
	if rules['domains']:
		for domain in rules['domains']:
			
			print(domain['name'].ljust(50) + (domain['ip'] or '[\033[1;31m404\033[0m] Run update to save'))
	else:
		print('There are no domains registered yet')





def print_help():
	print('''NAF-CE is based on a configuration file placed on /etc/naf/rules.json

Example of configuration file:

\033[1;32m{
	"allow_rule": "-A INPUT -s {ip} ACCEPT",
	"domains": [
		{
		"name": "domain.com",
		"ip": "8.8.8.8"
		}
	]
}\033[0m

NAF-CE check the domain resolution for each domain and add or delete the defined "allow_rule" rule replacing the {ip} keyword with the resolution of the domain name

''')

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'update':
			check_domains()
		elif sys.argv[1] == 'edit':
			edit_rules()
		elif sys.argv[1] == 'list':
			list_rules()
		else:
			print_help()
	else:
		print_help()
