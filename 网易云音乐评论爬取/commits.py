#coding:utf-8
#最小id应该是59867，最大id应该是1829999
#爬取歌曲评论并存入mysql数据库
'''
主要参考文章：https://www.zhihu.com/question/36081767
post加密部分也给出了，可以参考原帖：
作者：平胸小仙女
链接：https://www.zhihu.com/question/36081767/answer/140287795
来源：知乎
'''
import base64
import requests
import json
from Crypto.Cipher import AES
import time
import pymysql


#headers
headers = {
	'Host':"music.163.com",
	'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	'Accept-Encoding':"gzip, deflate",
	'Content-Type':"application/x-www-form-urlencoded",
	'Cookie': 'appver=1.5.0.75771;',
	'Connection':"keep-alive",
	'Referer': 'http://music.163.com/',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
	}
#构造第一个参数，参数与评论页面有关
def first_params(offset):
	first_para = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset,'false')
	return first_para

first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
second_param  =  '010001'
third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
forth_param = '0CoJUm6Qyw8W8jud'

#构造一个函数，获得h_encText
def get_params(first_param):
	iv  = '0102030405060708'
	first_key  =  forth_param
	second_key = 16 * 'F'
	h_encText = AES_encrypt(first_param, first_key, iv)
	h_encText = AES_encrypt(h_encText, second_key, iv)
	return h_encText
	
#encSecKey是一个常量
def get_encSecKey():
	#encSecKey = rsaEncrypt(secKey, pubKey, modulus)
	encSecKey = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
	return encSecKey

#对数据进行AES加密
def AES_encrypt(text, key, iv):
	pad = 16 - len(text) % 16
	text = text + pad * chr(pad)
	encryptor  =  AES.new(key, AES.MODE_CBC, iv)
	encrypt_text = encryptor.encrypt(text)
	encrypt_text = str(base64.b64encode(encrypt_text))
	return encrypt_text[2:-1]

#定义一个函数，获取json
def get_json(url, params, encSecKey):
	data = {
		"params": params,
		"encSecKey": encSecKey
	}
	
	response = requests.post(url=url, headers=headers, data=data)

	return response.content

#定义一个函数处理json数据
def inf(json):
	for item in json['comments']:
		userId = item['user']['userId']
		comment = item['content']
		get_db(userId, comment)

#定义一个函数，获取所有页面评论，并存入数据库
def get_all(total):
	if total > 20:
		page  = int(total/20)
		print(page)
		offset = 1
		while offset <= page:
			first_para = first_params(offset*20)
			param = get_params(first_para);
			json_tex = get_json(url, param, encSecKey)
			json_dic = json.loads(json_tex)
			inf(json_dic)
			# for item in json_dic['comments']:
				# print (item['content'])
			time.sleep(3)
			offset +=  1
	else:
		pass

#定义一个函数，进行数据库登陆,自己设置数据库
def dbhandle():
	conn = pymysql.connect(
		host = "127.0.0.1",
		user = "root",
		passwd = "*********",
		charset = "utf8",
		use_unicode = True
	)
	return conn

#定义一个函数，进行数据库数据存储
def get_db(it, items):
	dbobject = dbhandle()
	cursor = dbobject.cursor()
	cursor.execute("USE cloudnet")

	sql = "INSERT INTO cloud_items(userid, comment) VALUES(%s,%s)"
	try:
		cursor.execute(sql,(it,items))
		cursor.connection.commit()
	except BaseException as e:
		print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
		dbobject.rollback()

if __name__ == "__main__":
	start_time = time.time() 
	#url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_+'i'+?csrf_token='
	url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_1829999?csrf_token='
	params = get_params(first_param);
	encSecKey = get_encSecKey();
	json_text = get_json(url, params, encSecKey)
	json_dict = json.loads(json_text)
	total = json_dict['total']
	inf(json_dict)
	get_all(total)
	end_time = time.time() 
	print('总耗时：%f'%(end_time - start_time))


