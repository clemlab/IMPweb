import requests

import json

def domain_smush(dom):
	data = ''
	for i in dom:
		data += i + '.'
	return data[:-1]

def acaemail_verify(domain):
	domain = domain.split('.')
	domains = [domain_smush(domain[-2:]), domain_smush(domain[-3:])]
	if verify_academy(domains[0]) == 1 or verify_academy(domains[1]) == 1:
		return True
	return False


def verify_academy(domain):
	'''
	make a query to academic domains to see if the provided email is valid
	'''
	url = "http://127.0.0.1:5000/search?domain=" + domain
	response = requests.get(url)
	data = json.loads(response.content)
	return len(data)


