#coding:utf-8

import requests
import os
import re
import base64
from fontTools.ttLib import TTFont


	
def get_html(url):
	headers ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'no-cache',
	'Connection': 'keep-alive',
	'Host': 'www.shixiseng.com',
	'Pragma': 'no-cache',
	'Referer': 'https://www.shixiseng.com/cd',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

	sessions = requests.session()
	response = sessions.get(url=url,headers=headers)

	return (response.content.decode('utf-8'))
	
def get_content(response):
	name = r'data-desc="search-职位名称">(.*?)</a>'
	names = re.findall(name,str(response))
	base64 = r'base64,(.*?)"\)}'
	base64_code = re.findall(base64,str(response))
	base_str = base64_code[0]
	#print(base_str)
	import base64
	base = base64.b64decode(base_str)
	print(base_str)
	with open('f.ttf','wb') as f:
		f.write(base)
		f.close()

	return names
	#print(names)
	#print(base64_code)
	
	
def convert_ttf():
	
	font = TTFont('f.ttf')
	font.saveXML('f.xml')
	font_list = font.getGlyphOrder()
	return font_list

def get_xml_content(font_list):
	codes = {}
	with open('f.xml','r') as f:
		content = f.read()
		for i in font_list:
			n = i.replace('uni','')
			xml_re = r'<map code="(.*)" name="'+i+'"/>'
			code = re.search(xml_re,str(content)).group(1)
			co = code.replace('0x','&#x')
			codes[co] = chr(int(n,16))
			print(co)
	print(codes)
	return codes
		

		
		
def main():
	name = []
	url = 'https://www.shixiseng.com/interns?k=Python&p=1'
	response = get_html(url)
	names = get_content(response)
	#print(names)
	font_list = convert_ttf()
	codes = get_xml_content(font_list[2:])
	for i in names:
		for key in codes:
				if key in i:
					i = i.replace(key,codes[key])
		print(i)
		name.append(i)
	
	with open('names.txt','w') as f:
		f.write(str(name))
		f.close()
			
		

if __name__ == '__main__':
	main()
	