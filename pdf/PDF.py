#coding=utf-8
import requests
import pdfkit
import re
import os
import time
from PyPDF2 import PdfFileMerger
from bs4 import BeautifulSoup

#定义一个函数来获取左边的网页列表，注意，获取到的列表是相对链接，要转为绝对链接
def get_url_list(first_url, headers):
	sessions = requests.session()
	response = sessions.get(url = first_url, headers=headers)
	s  = r'<a href="(.*?)" target="_top">'
	body = re.findall(s, str(response.content))
	return body

#定义一个函数，将相对链接转为绝对链接并返回url
def get_url(url_lists):
	url = []
	for i in url_lists:
		url.append('https://code.ziqiangxuetang.com/django/'+i)
	return url
	
#定义一个函数，获取网页中的图片
def get_pic(url):
	sessions = requests.session()
	for i in url:
		pic =  sessions.get('https://code.ziqiangxuetang.com/media/uploads/images/'+i).content
		z = 'C:\\media\\uploads\\images\\'+ i
		with open(z, 'wb') as f:
			f.write(pic)
			f.close()

#定义一个函数，写入网页正文，并且判断网页中是否含有照片，有照片就传入参数给get_pic函数，下载照片，然后将写入的html参数，和保存的pdf参数传入save_pdf函数
def cwrite(content,i):
	#这里添加判断，是因为，他最后有一个其他网页，用#来寻找，写入的时候会出错
	if '#' in i:
		i = 'https://code.ziqiangxuetang.com/django/x.html'
	else:
		pass
	with open(i.split('/',4)[4], "w", encoding="utf-8") as f:
		if 'src="/media/uploads/images/' in str(content):
			pic_url = re.findall('src="/media/uploads/images/(.*?)"',str(content))
			for url in pic_url:
				get_pic(pic_url)
		else:
			pass
		f.write(str(content))
		f.close()
	#保存pdf时为了方便下一步合并，所以采用时间来命名，保证文档的连续性
	save_pdf(i.split('/',4)[4],str(time.time())+".pdf")

#定义一个函数，来获网页正文
def get_content(urls, headers):
	sessions = requests.session()
	for i in urls:
		if 'target' not in i:
			response = sessions.get(i, headers=headers)
			soup = BeautifulSoup(response.content, 'html.parser')
			content = soup.find_all(id="main_content")
			cwrite(content, i)
			time.sleep(3)

#定义个一个函数，将保存的html转化成pdf
def save_pdf(htmls, file_name):
	options = {
		'page-size': 'Letter',
		'encoding': "UTF-8",
		'custom-header': [
			('Accept-Encoding', 'gzip')
		]
	}
	config=pdfkit.configuration(wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
	pdfkit.from_file(htmls, file_name, configuration = config, options=options)

#定义一个函数来合并刚才生成的pdf，输出为‘django.pdf’
def get_pdf():
	options = {
			'page-size': 'Letter',
			'encoding': "UTF-8",
			'custom-header': [
				('Accept-Encoding', 'gzip')
			]
		}
	#因为是在win10下写的，然后产生了报错，寻找原因，是要配置wkhtmltopdf，将下面的绝对路径下的exe执行程序换成你安装目录下的执行程序，注意，是绝对路径
	config=pdfkit.configuration(wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
	#这里可以添加绝对目录，不选择则是在此目录下寻找，例如我这儿写了一个绝对目录。
	root = 'C:\\Users\\12711\\Desktop\\pdf'
	merger  =  PdfFileMerger()
	a=[]
	for i in os.listdir(root):
		print(i)
		if '.pdf' in i:
			merger.append(open(i, 'rb'))
	merger.write(open('django.pdf','wb'))

#主函数
if __name__ == '__main__':
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding':'zip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Connection':'keep-alive',
		'Host':'code.ziqiangxuetang.com',
		'Referer':'https://code.ziqiangxuetang.com/django/django-tutorial.html',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		}
	first_url = 'https://code.ziqiangxuetang.com/django/django-tutorial.html'
	url_lists = get_url_list(first_url,headers)
	urls = get_url(url_lists)
	get_content(urls, headers)
	get_pdf()
	