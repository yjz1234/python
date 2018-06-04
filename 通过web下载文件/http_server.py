#coding:utf-8
#在运行的目录下生成http服务，访问并下载文件。
import os
import re

from http.server import \
	BaseHTTPRequestHandler, HTTPServer

from urllib.parse import quote, unquote

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			u = unquote(self.path)
			list = os.listdir(os.getcwd()+u.replace('/','\\'))
			self.send_response(200)
			self.send_header('Content-type','text/html; charset=utf-8')
			self.end_headers()
			for i in list:
				if os.path.isfile(os.getcwd()+u.replace('/','\\')+i):
					self.wfile.write(('<li><a href='+self.path+quote(i)+'>'+i+'</a></li>').encode())
				else:
					self.wfile.write(('<li><a href='+self.path+quote(i)+'/>'+i+'</a></li>').encode())
			self.wfile.write(('<li><form id="form1" action="upload" target="frame1" method="post" enctype="multipart/form-data"> <input type="file" name="file"> <input type="submit" value="上传"> </form></li>').encode())
		except:
			#self.send_error(404,'File not Found:%s'%self.path)
			f = open(os.getcwd()+unquote(self.path).replace('/','\\'),'rb')
			self.send_response(200)
			self.send_header('Content-type','application/octet-stream')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			
	def do_POST(self):
		#try:
			r = 'filename="(.*)"'
			self.send_response(200)
			self.send_header('Content-type','text/html; charset=utf-8')
			self.end_headers()
			self.wfile.write(('上传成功').encode())
			a = self.rfile.readline()
			b = self.rfile.readline()
			self.rfile.readline()
			self.rfile.readline()
			filename = re.search(r,b.decode('utf-8')).group(1)
			print(filename)
			with open (filename,'ab') as f:
				while True:
					read=self.rfile.readline()
					if '------WebKitFormBoundary' in str(read):
						break
					print(read)
					if read:
						f.write(read)
				f.close()

		# except:
			# print(1)
			

def main():
	try:
		server = HTTPServer(('',80), MyHandler)
		print('welcome')
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		
if __name__ == '__main__':
	main()