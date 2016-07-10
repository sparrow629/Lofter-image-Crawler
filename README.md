# Lofter-image-Crawler
Author: Sparrow 
Purpose: downloading image from www.lofter.com in every blog's page once avoiding download image one by one. 
Created: 2016-7.9 

Introduction:
This is supportted by Python 2.7 I can not guarrentee the stablist. So far, I only use this script in Mac OS 10.11.15. User, should type the URL whose lofter blog, can either copy the main blog's url, such as "http://yudengyue.lofter.com/", or copy any other child url, such as "http://yudengyue.lofter.com/post/1d877536_b942107". The image will download in the file named as "Lofterimgdownload" of the directory where you put this .py file in. You can modify the regular expression in the function of getImg() according to the html tag in different kind of pages to fit your needs. It is just a simple edition of crawler, which can be easily modify to crawler other website. I may give more specific crawler according to specific site such as baidutieba.

The new function is that there are two more mode.  Mode 1 you can download any current page like the url format as "http://yudengyue.lofter.com/?page=2&t=1466499686554". What's more, Mode 2, you can download all the images of one's blog once with type the main URL such as "http://yudengyue.lofter.com/", which is more convenient for restore all the image.
And you can just pick any postpages to download current page's images directly. It can crawle most of different css styles of lofter.

Downloading file:
For Mac OS:
Download the Lofter_image_crawler.py to your local computer with python 2.7. Open your terminal cd into where you put this .py file. Then type "python Lofter_image_crawler.py" you can run it simply.

For Windows OS:
Latest "Lofter-image-crawler.exe.zip" file is a executable file on Windows OS, I only test on the Win8. You can just input the url of any lofter blogs directly with this .exe program.
Also you can python .py file better with python 2.7.

If there is any problem, leave me a message.

