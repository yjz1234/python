#-*- coding：utf-8 -*-
import urllib.request
import urllib.parse
import re
import time
import os
if not os.path.exists('E:\\qiushibaike'):
	os.makedirs('E:\\qiushibaike')
url = "http://www.qiushibaike.com/text/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36","Referer":"http://www.qiushibaike.com/text/"}
request=urllib.request.Request(url=url,headers=headers)
response=urllib.request.urlopen(request)
html_source = response.read().decode('utf-8')
file = open('E:\\qiushibaike\\qiushibaike.txt','w')
title=r'<div class="content">(.*?)</div>'
body = re.findall(title,html_source,re.S|re.M)
for line in body:
	body_source=r'<span>(.*?)</span>'
	body_zz = re.compile(body_source,re.S|re.M)
	contents=re.search(body_zz,line)
	content=contents.group()
	contentss = content.strip('<br>,<span>')
	contentsss = contentss.replace('<br/>','')
	contentssss =contentsss.rstrip('</')
	file.write(contentssss+"\n"+"\n")
file.close()