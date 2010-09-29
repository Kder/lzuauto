#!/usr/bin/env python
#-*-coding=utf-8-*
from pytesser import *
import urllib, httplib, time, re, sys


headers = {"User-Agetn":"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100916 Firefox/3.6.10","Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Keep-Alive":"115","Connection":"keep-alive"}
conn = httplib.HTTPConnection( "a.lzu.edu.cn" )  
conn.request( 'GET', '/', headers = headers )
response = conn.getresponse()
print response.getheaders()
cookie = response.getheader('set-cookie').split()[0]
temp = {'Cookie':cookie}
headers.update(temp)
conn.close()

# image = Image.open('code.jpg')
# s = image_to_string(image)[0:4]
# print s[0:4]