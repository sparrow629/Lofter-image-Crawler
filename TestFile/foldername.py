#!/usr/bin/python
import re 
import urllib
import os

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def foldername(html,url):
	reg_month = r'<div class="month">(.*?)</div>'
	month = re.compile(reg_month)
	time_month = re.findall(month, html)
	reg_date = r'<div class="date">(.*?)</div>'
	date = re.compile(reg_date)
	time_date = re.findall(date, html)
	reg_year = r'<div class="year">(.*?)</div>'
	year = re.compile(reg_year)
	time_year = re.findall(year, html)
	postfix = '.lofter.com'
	blogname = url[7:url.index(postfix)]
	# print blogname
	# print time_month
	# print time_date
	# print time_year
	foldername = blogname +"-" + time_year[0] +"-"+ time_month[0] +"-"+ time_date[0]
	imgpath = r'/Users/sparrow/Desktop/demo/jpgcrawler/%s' % (foldername)
	if not os.path.exists(imgpath):
		os.makedirs(imgpath)
	return imgpath

html = getHtml("http://sexvvip.lofter.com/?page=2&t=1467794880000")
print foldername(html, "http://sexvvip.lofter.com/?page=2&t=1467794880000")
