#!/usr/bin/python
#coding:utf-8
"""
  Author:  Sparrow
  Purpose: downloading image from www.lofter.com in every blog's page once.
  Created: 2016-7.4
"""

import multiprocessing
import re
import urllib
import time
import os
import threading


def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getImg(html,url,posturl):
	global Number

	reg = r'src="(.*?\.jpe*?g\?.*?)"'
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
			Name = Postname + '_' + str(i)

			target = path + '%s.jpg' % Name
			i += 1
			print "Downloading %s " % target
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
	if postnamelist:
		return postnamelist[0]
	else:
		postnamelist = ['page1']
		return postnamelist[0]

def home(url):
	reg = r'http://.*?\.lofter\.com/post/.*'
	h = re.compile(reg)
	jhome = re.findall(h,url)
	print jhome
	if jhome :
		print 'Post'
		return False
	else:
		print 'Homepage'
		return True

def getnexturl(url):
	html = getHtml(url)
	reg = r'<a href="(\?page=.+?\&t=\d.*?)"'
	pageturl = re.compile(reg)
	pagepostfix = re.findall(pageturl, html)
	if pagepostfix:
		nexturl = pagelists[0] + pagepostfix[0]
		return nexturl

	else:
		print 'There is no more page'
		return False

class ThreadTask(threading.Thread):

	def __init__(self, PostUrlList):
		super(ThreadTask, self).__init__()
		self.postUrllist = PostUrlList

	def run(self):
		for posturl in self.postUrllist:
			try:
				print(posturl)
				getImg(getHtml(posturl),URL, posturl)
			except:
				print('Something wrong in post %s' % posturl)

def BlogDownload(URL):
	Task = []
	global pagelists
	pagelists = [URL]

	nexturl = getnexturl(URL)
	while nexturl:
		pagelists.append(nexturl)
		print nexturl, "Adding page %s" % len(pagelists)
		nexturl = getnexturl(nexturl)
	print pagelists

	pagenumber = len(pagelists)

	for page in range(0,pagenumber):
		url = pagelists[page]
		html = getHtml(url)
		print "Downloading Page %s" % (page + 1)

		PostUrllist = getPost(html)

		task = ThreadTask(PostUrllist)
		Task.append(task)
		print '-'*16,"\nThis is thread %s \n "% page,'-'*16

	for task in Task:
		task.setDaemon(True)
		task.start()
		print(time.ctime(),'thread %s start' % task)
	for task in Task:
		task.join()
	while 1:
		for task in Task:
			if task.is_alive():
				continue
			else:
				Task.remove(task)
				print(time.ctime(),'thread %s is finished' % task)
		if len(Task) == 0:
			break



if __name__ == '__main__':

	select = 'N'
	while (select == 'N'):
		print '''
		---------------------------------
		Welcome to lofter image download!
		---------------------------------
		Author:  Sparrow
  		Purpose: downloading images from xxx.lofter.com once.
  		Created: 2016-7.4
		'''
		URL = raw_input('Input url: ')
		html = getHtml(URL)

		Count = 0

		if home(URL):
			print '''
			which mode you want:
			1.Downloading current page's images.
			2.Downloading all the images from current page to the end of this blog once.
			Notice: If you want to download the entire blog's images, you should copy the format like "http://xxxxxx.lofter.com/"
			'''
			Mode = int(raw_input())
			if Mode == 1:
				PostUrllist = getPost(html)
				Postnumber =  len(PostUrllist)
				print Postnumber

				for posturl in PostUrllist:
					html = getHtml(posturl)
					getImg(html, URL, posturl)

			if Mode == 2:

				BlogDownload(URL)

		else:
			post_url = URL
			getImg(html,URL,post_url)


		select = raw_input("Do you want to quit? [Y/N]")


