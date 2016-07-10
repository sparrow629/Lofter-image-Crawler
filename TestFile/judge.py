#!/usr/bin/python
import re 


def home(url):
	reg = r'http://.*?\.lofter\.com/\?+.*'
	h = re.compile(reg)
	jhome = re.findall(h,url)
	print jhome
	if jhome :
		print 'true'
		return True
	else:
		print 'false'
		return False

# URL = raw_input('Input url: ')
URL = 'http://billsparrow.lofter.com/post/18d706_b86838d'
print home(URL)
