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

def getImg(html,url,posturl):
	global Number

	reg = r'src="(.*?\.jpg\?.*?)"'
	imgre = re.compile(reg)
	imglist_none = re.findall(imgre, html)
	imglist = list(set(imglist_none))
	# return imglist 
	postfix = '.lofter.com'
	blogname = url[7:url.index(postfix)]
	path = 'Lofterimgdownload/%s' % (blogname)
	if not os.path.exists(path):
		os.makedirs(path)
	if imglist:
		Name = getPostname(posturl)

		print len(imglist)
		print imglist
		i = 0
		for imgurl in imglist:
			Number += 1
			print "Downloading %s image" % (Name+str(i))
			target = path + '%s.jpg' % (Name+str(i))
			i += 1
			# urllib.urlretrieve(imgurl, target)

	else:
		print 'There is no image!'

def getPost(html):
	reg = r'href="(http://.*?\/post\/.*?)"'
	posturl = re.compile(reg)
	posturllist = re.findall(posturl, html)
	return list(set(posturllist))

def getPostname(posturl):
	reg = r'http://.*?\/post\/(.*)'
	postname = re.compile(reg)
	postnamelist = re.findall(postname, posturl)
	print postnamelist
	return postnamelist[0]

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

	global Number
	Number = 0

	if home(URL):
		# print getImg(html)
		print getPost(html)
		print len(getPost(html))
		Posturl = getPost(html)
		for post_url in Posturl:
			imghtml = getHtml(post_url)
			# print len(getImg(imghtml))
			getImg(imghtml,URL,post_url)
		print "Downloading %s images" % Number
	else:
		post_url = URL
		getImg(html,URL,post_url)


