#!/usr/bin/python
#coding:utf-8
"""
  Author:  Sparrow
  Purpose: downloading image from www.lofter.com in every blog's page once.
  Created: 2016-7.4
"""
import re 
import urllib
import time
import os

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getImg(html):
	reg = r'src="(.*?\.jpg\?.*?)"'
	imgre = re.compile(reg)
	imglist_none = re.findall(imgre, html)
	imglist = list(set(imglist_none))
	# return imglist 
	path = 'Lofterimgdownload/'
	if not os.path.exists(path):
		os.makedirs(path)
	if imglist:
		x = time.time()
		print len(imglist)
		# print imglist
		for imgurl in imglist:
			print "Downloading %s image" % x
			target = path + '%s.jpg' % x
			urllib.urlretrieve(imgurl, target)
			x+=1
	else:
		print 'There is no image!'

def getPost(html):
	reg = r'href="(http://.*?\/post\/.*?)"'
	posturl = re.compile(reg)
	posturllist = re.findall(posturl, html)
	return list(set(posturllist))

def home(url):
	reg = r'http://.*?\.lofter\.com/$'
	h = re.compile(reg)
	jhome = re.findall(h,url)
	print jhome
	if jhome :
		print 'true'
		return True
	else:
		print 'false'
		return False

if __name__ == '__main__':
	URL = raw_input('Input url: ')
	html = getHtml(URL)
	if home(URL):
		# print getImg(html)
		print getPost(html)
		print len(getPost(html))
		Posturl = getPost(html)
		for post_url in Posturl:
			imghtml = getHtml(post_url)
			# print len(getImg(imghtml))
			getImg(imghtml)
	else:
		getImg(html)


