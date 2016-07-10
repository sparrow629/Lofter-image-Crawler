#!/usr/bin/python
import re 
import urllib
import time
import os

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getImg(html):
	reg = r'src="(.*?\.jpg.*?stripmeta\=0)"'
	imgre = re.compile(reg)
	imglist_none = re.findall(imgre, html)
	imglist = list(set(imglist_none))
	# return imglist 
	path = 'Lofterimgdownload/'
	if not os.path.exists(path):
		os.makedirs(path)
	x = 0
	for imgurl in imglist:
		target = path + '%s.jpg' % x
		urllib.urlretrieve(imgurl, target)
		x+=1

html = getHtml("http://sexvvip.lofter.com/post/1ddcf60c_b87d9b4")
getImg(html)
