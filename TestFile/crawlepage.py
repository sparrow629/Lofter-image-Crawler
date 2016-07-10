import re 
import urllib
import time
import os

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getnexturl(url):
	html = getHtml(url)
	reg = r'<a href="(\?page=.+?\&t=\d.*?)"'
	pageturl = re.compile(reg)
	page = re.findall(pageturl, html)
	if page:
		nexturl = pagelists[0] + page[(len(page)-1)]
		pagelists.append(nexturl)
		print nexturl,"adding page %s" % len(pagelists)
		getnexturl(nexturl)
		return pagelists

	else:
		print 'There is no more page'
		return False



if __name__ == '__main__':
	url = 'http://sexvvip.lofter.com/'
	pagelists = [url]
	print getnexturl(url)

