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
	path = 'Lofterimgdownload/%s/' % (blogname)
	if not os.path.exists(path):
		os.makedirs(path)

	if imglist:
		Postname = getPostname(posturl)
		print len(imglist)
		# print imglist
		i = 0
		for imgurl in imglist:
			Number += 1
			Name = Postname + '_' + str(i)
			print "Downloading %s image" % Name
			target = path + '%s.jpg' % Name
			i += 1
			print target
			urllib.urlretrieve(imgurl, target)
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
	URL = raw_input('Input url: ')
	html = getHtml(URL)

	global Number
	Number = 0

	if home(URL):
		print '''
			which mode you want:
			1.Downloading current page's images.
			2.Downloading all the images from current page to the end of this blog once.
			Notice: If you want to download the entire blog's images, you should copy the
			the format like "http://xxxxxx.lofter.com/"
		'''
		Mode = int(raw_input())
		if Mode == 1:
			print getPost(html)
			print len(getPost(html))
			Posturl = getPost(html)
			for post_url in Posturl:
				imghtml = getHtml(post_url)
				getImg(imghtml,URL,post_url)
			print "Congratulation! Totally finished downloading %s images" % Number
		if Mode == 2:
			pagelists = [URL]
			i = 1
			print getnexturl(URL)
			for nexturl in pagelists:
				nexthtml = getHtml(nexturl)
				print "Downloading Page %s" % i
				i +=1
				print getPost(html)
				print len(getPost(html))
				Posturl = getPost(html)
				for post_url in Posturl:
					imghtml = getHtml(post_url)
					getImg(imghtml,URL,post_url)
			print "Congratulation! Totally finished downloading %s images" % Number

	else:
		post_url = URL
		getImg(html,URL,post_url)
		print "Congratulation! Totally finished downloading %s images" % Number


