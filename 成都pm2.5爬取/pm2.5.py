#coding:utf-8
import requests
import re
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import pymysql

#定义一个函数，用于登陆数据库
def dbhandle():
	conn = pymysql.connect(
		host = "127.0.0.1",
		user = "root",
		passwd = "*******",
		charset = "utf8",
		use_unicode = True
	)
	return conn

#定义一个函数，进行数据库数据存储，存储格式 '城市加时间'，'aqi'
def save_mysql(utime, aqi):
	dbobject = dbhandle()
	cursor = dbobject.cursor()
	cursor.execute("USE pm2")
	
	#这句提供了IGNORE选项，因为部分数据可能更新不及时，所以重复就不插入
	sql = "INSERT IGNORE INTO pm2(Time, Aqi) VALUES(%s,%s)"
	try:
		cursor.execute(sql,(utime,aqi))
		cursor.connection.commit()
	except BaseException as e:
		print("错误>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误")
		dbobject.rollback()

#定义一个函数获取pm2.5的数据，并最后返回一个aqi的元组，用于计算平均值 
def get_pm(url):
	headers = {'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Connection':'keep-alive',
		'Host':'api.waqi.info',
		'Origin':'http://aqicn.org',
		'Referer':'http://aqicn.org/city/chengdu/us-consulate/cn/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
	response = requests.get(url = url,headers = headers)
	json_dict = json.loads(response.content)
	aqis = []
	for city in json_dict:
		utime = city['city'] + city['utime'] 
		aqi = city['aqi']
		if '-' not in aqi:
			aqis.append(aqi)
		save_mysql(utime, aqi)
	return aqis

#定义一个函数，用于计算aqi平均值
def av(aqis):
	aqiss = 0
	for aqi in aqis:
		aqiss = int(aqi) + aqiss
	return aqiss/len(aqis)
	
#定义一个函数，用于发送邮件，此处采用的是qq邮箱，其他的邮箱方式和端口自行搜索，但大同小异
def send_mail(avqi):
	#qq邮箱smtp服务器
	host_server = 'smtp.qq.com'
	
	#sender_qq为发件人的qq号码
	sender_qq = '1931048746'
	
	#pwd为qq邮箱的授权码
	pwd = '********'
	
	#发件人的邮箱
	sender_qq_mail = '1931048746@qq.com'
	
	#收件人邮箱
	receiver = '1271161774@qq.com'
	
	#邮件的正文内容
	mail_content = '成都现在平均pm为' + str(avqi) +'\n101-150 三级（轻度污染) \n 151-200 四级（中度污染） \n201-300五级（重度污染）\n300+ 六级（严重污染）'
	#邮件标题
	mail_title = 'pm2.5'
	
	#ssl登录
	smtp = SMTP_SSL(host_server)
	
	#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
	smtp.set_debuglevel(0)
	smtp.ehlo(host_server)
	smtp.login(sender_qq, pwd)
	msg = MIMEText(mail_content, "plain", 'utf-8')
	msg["Subject"] = Header(mail_title, 'utf-8')
	msg["From"] = sender_qq_mail
	msg["To"] = receiver
	smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
	smtp.quit()

#主函数 
if __name__ == "__main__":
	url = 'https://api.waqi.info/mapq/bounds/?bounds=30.4687977564324,103.62442016601561,30.846826454247694,104.43328857421875'
	aqis = get_pm(url)
	avqi = av(aqis)
	#平均值大于150，就可以发送邮件，可以自行设定
	if avqi >=150:
		send_mail(avqi)
	

