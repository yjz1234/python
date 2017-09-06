#coding:utf-8
from bs4 import BeautifulSoup
import re 
import time
import requests
#以上是导入模块

#requests的用法，优点是能记录cookie，下次发送时自动补充
sessions = requests.session()

#关键词，提取的关键词，预先赋值
s = '新生'
#定义一个函数爬取贴吧帖子网址及标题
def get(f):
	x = f*50
	#因为贴吧网页的变化是与最后一项 pn=  的值有关，所以预先根据想要爬取的页数生成url
	url = 'http://tieba.baidu.com/f?kw=成都大学&ie=utf-8'+'&pn='+str(x)

	#headers，防止被百度禁止爬取，所以加上
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Host':'tieba.baidu.com'
		}
	
	#爬取的回应的内容，使用beautifulsoup解析，可以使用其他模块解析
	response = sessions.get(url=url, headers=headers)
	res = BeautifulSoup(response.content, 'html.parser')

	#网页的正则表达式，根据正则表达式提取所需的帖子标题，暂未写网页的，提取思路是：提取<a>标签内容，然后分别再次提取title与href
	#s = r'title="(.*?)" target="_blank" class="j_th_tit "'
	s = r'<a href=(.*?)" target="_blank" class="j_th_tit "'
	title = re.findall(s, str(res))
	#返回title给下一个函数作为参数
	return title


#定义一个函数处理爬取网页后的数据
def handle(title):
	#遍历title列表中的所有元素，并赋予i
	for i in title:
		#判断关键词即s='出租'是否包含在i中，包含就执行
		if s in i:
			z=i.replace('"','')
			ss = 'http://tieba.baidu.com'+z.replace('title=','')
			url = ss.split(' ')[0]
			print(ss)
			return url

#定义一个函数获取帖子内容
def get_body(url):
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

	response_body = sessions.get(url=url,headers=headers)
	res_body = BeautifulSoup(response_body.content,'html.parser')
	#正则，略显复杂，因为不少人回复帖子喜欢加入图片，因此先预处理
	c = r' class="d_post_content j_d_post_content clearfix"(.*?)</div>'
	#c = r'<div(.*?)</div>'	
	body = re.findall(c, str(res_body))
	
	#遍历第一遍预处理的内容
	for i in body:
		#根据处理内容，用空格分割，分两次
		bodys = i.split(' ',2)
		#过滤所有含图片的内容
		if '<img' not in bodys[2]:
			#打印帖子内容
			print(bodys[2])
#主函数	
if __name__ == '__main__':
	#根据想要爬取的页数进行循环。
	f=1
	while f<=3:
		title = get(f)
		url = handle(title)
		get_body(url)
		f = f+1
		
		#延时函数，防止因为过度的访问造成服务器拥堵而被禁止
		time.sleep(3)
		
	
	
