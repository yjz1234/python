#-*- coding：utf-8 -*-
import urllib.request
import urllib.parse
import re
import time
import os
n = 1
while n<=5:
	if not os.path.exists('E:\\Picture3'):
		os.makedirs('E:\\Picture3')
	url = "http://www.qiushibaike.com/imgrank/page/"+str(n)+"/"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36","Referer":"http://www.qiushibaike.com/imgrank/"}
	request=urllib.request.Request(url=url,headers=headers)
	response=urllib.request.urlopen(request)
	html_source = response.read().decode('utf-8')
	title = r'<img src="http://pic.qiushibaike.com/system/pictures(.*?).jpg"'
	body = re.findall(title,html_source)
	for line in body:
		content = 'http://pic.qiushibaike.com/system/pictures'+line+'.jpg'
		print(content)
		filename = os.path.basename(content)
		urllib.request.urlretrieve(content,'E:\\Picture3\\'+filename)
	n=n+1

	
