#user/bin/python3
#coding:utf-8
from pexpect import pxssh
import re

#自定义一个类，使用pxssh进行ssh连接，简化操作
class ssh:
	def __init__(self,host,user,password):
		self.user=user
		self.host=host
		self.password=password
		self.s=None
	#先要执行连接，才能继续下一步的查询
	def connect(self):
		try:
			self.s = pxssh.pxssh()
			self.s.login(self.host,self.user,self.password)
			return self.s
		except:
			print("error,please check ")

	def mem_info(self,cmd='cat /proc/meminfo'):
		s=self.s
		s.sendline(cmd)
		s.prompt()
		mem=s.before.decode('utf-8').split('\r\n')
		return  int(re.findall('(\d+)',mem[3])[0])
	
	def cpu_info(self,cmd='cat /proc/cpuinfo'):
		s=self.s
		s.sendline(cmd)
		s.prompt()
		cpu=(s.before.decode('utf-8'))
		print(cpu)
	
	def quit(self):
		self.s.close()



