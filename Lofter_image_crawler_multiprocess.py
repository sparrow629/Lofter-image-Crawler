#!/usr/bin/python
#coding:utf-8
"""
  Author:  Sparrow
  Purpose: downloading image from www.lofter.com in every blog's page once.
  Created: 2016-7.4
"""
from multiprocessing import Pool, Manager
import multiprocessing
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
		countQueue.put(i)
	else:
		print 'There is no image!'

	print('''
	-------------------------------------
	      Process ID: %s finished
	--------------------------------------
	''' % os.getpid())

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



class multiProcess(multiprocessing.Process):
	"""docstring for multiProcess"""
	def __init__(self, func, arg, url):
		super(multiProcess, self).__init__()
		self.func = func
		self.arg = arg
		self.URL = url

	def downloadworks(self):
		worknum = len(self.arg)
		p = multiprocessing.Pool(worknum)

		for i in range(worknum):
			post_url = self.arg[i]
			imghtml = getHtml(post_url)
			p.apply_async( self.func, args = (imghtml,self.URL,post_url,))

		p.close()
		# p.terminate()
		p.join()

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

		Time = 0

		Count = 0
		manager = Manager()
		countQueue = manager.Queue()

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

				Time = time.time()

				DownloadImage = multiProcess(getImg,PostUrllist,URL)
				DownloadImage.downloadworks()
				for i in range(Postnumber):
					Count += countQueue.get(True)

				print time.time()-Time

				print "Congratulation! Totally finished downloading %s images" % Count
			if Mode == 2:

				pagelists = [URL]
				i = 1
				Time = time.time()
				nexturl = getnexturl(URL)
				while nexturl:
					pagelists.append(nexturl)
					print nexturl, "Adding page %s" % len(pagelists)
					nexturl = getnexturl(nexturl)
				print pagelists

				pagenumber = len(pagelists)

				Number = []

				for page in range(0,pagenumber):

					url = pagelists[page]
					html = getHtml(url)
					print "Downloading Page %s" % (page + 1)

					PostUrllist = getPost(html)
					Postnumber = len(PostUrllist)
					print PostUrllist
					print Postnumber

					DownloadImage = multiProcess(getImg, PostUrllist, URL)
					DownloadImage.downloadworks()
					Number.append(page)
					Number[page] = 0
					for i in range(Postnumber):
						Number[page] += countQueue.get(True)

					print "This page download %s images" % Number[page]
					Count += Number[page]

				print time.time() - Time
				print "Congratulation! Totally finished downloading %s images" % Count

		else:
			post_url = URL
			getImg(html,URL,post_url)
			Count = countQueue.get(True)
			print "Congratulation! Totally finished downloading %s images" % Count

		select = raw_input("Do you want to quit? [Y/N]")


