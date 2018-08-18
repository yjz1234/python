#coding:utf-8

import pymysql

class database:
	def __init__(self,host,username,password):
		self.host = host
		self.username = username
		self.password = password
		self.conn=None
		self.cursor = None

	#定义一个函数获取游标,连接数据库
	def my_connect(self):
		my_conn = pymysql.connect(
			host = self.host,
			user = self.username,
			passwd = self.password,
			charset = "utf8",
			use_unicode = True
		)
		self.conn=my_conn
		self.cursor=my_conn.cursor()
	#功能:创建数据库
	def create_database(self,database):
		self.cursor.execute('CREATE DATABASE %s;'%database)
		
	#功能:选择数据库,执行数据库之内的操作必须先选择数据库
	def use_database(self,database):
		self.cursor.execute('USE %s;'%database)
		
	#功能:删除数据库
	def drop_database(self,database):
		self.cursor.execute('DROP DATABASE %s;'%database)

	#功能:创建表
	def create_table(self,table_name,content):
		self.cursor.execute('CREATE TABLE %s(%s);'%(table_name,content))
		
	#功能:删除表，需要在之前选择数据库
	def drop_table(selfe,table_name):
		self.cursor.execute('DROP %s;'%table_name)
		
	#功能:删除数据，condition为限制条件，同样需要先选择数据库
	def delete_data(self,table_name,condition):
		self.cursor.execute('DELETE FROM %s WHERE %s;'%(table_name,condition))
		
	#功能:导出数据表，需要先选择数据库
	def table_out(self,table_name,outfile):
		self.cursor.execute('SELECT * FROM %s INTO OUTFILE \'%s\';'%(table_name,outfile))

	#功能:导入数据
	def source_file(self,filename):
		self.cursor.execute('SOURCE \'%s\';'%filename)
		
	#功能：简单查询，condition同样为限制条件
	def select_data(self,table_name,condition):
		self.cursor.execute('SELECT * FROM %s WHERE %s;'%(table_name,condition))
		for i in self.cursor.fetchall():
			print(i)
	#功能：改变表名
	def alter_table_name(self,old_table,new_table):
		self.cursor.execute('ALTER TABLE %s RENAME %s;'%(old_table,new_table))

	#功能：改变字段名
	def alter_table_change(self,table_name,old_modify,new_modify,data_type=''):
		self.execute('ALTER TABLE %s CHANGE %s %s %s %s;'%(table_name,old_modify,new_modify,data_type))
		
	#功能：改变字段
	def alter_table_modify(self,table_name,modify,data_type=''):
		self.execute('ALTER TABLE %s MODIFY %s %s;'%(table_name,modify,data_type))
		
	#退出
	def quit(self):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()
		
