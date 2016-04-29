



def silly_script(string):
	return string[::-1]

def saniscript(string):
	sanitary = ''
	for element in string:
		if element == 'a':
			sanitary += 't'
		elif element == 'g':
			sanitary += 'c'
		elif element == 'c':
			sanitary += 'g'
		elif element == 't':
			sanitary += 'a'
		else:	
			return 'Invalid DNA sequence'
	return sanitary