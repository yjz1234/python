#user/bin/python3
#coding:utf-8

import matplotlib.pyplot as plt
import numpy as np
import time
from ssh import *

y=[]
x=[]
plt.ion()
fig = plt.figure()
ax1=fig.add_subplot(111)
line, = ax1.plot(x,y,linestyle='-',color='r')


def connect():
	s=ssh('127.0.0.1','root','******')
	s.connect()
	return s



def paint(i,a):
	y.append(a)
	x.append(i)
	if i % 30 == 0:
		del  y[:10]
		del  x[:10]
	ax1.set_ylim(min(y), max(y) + 1)
	ax1.set_xlim(min(x[-20:]), max(x[-20:]) + 1)
	plt.pause(1)
	line.set_data(x[-20:],y[-20:])
	ax1.figure.canvas.draw()


def main():
	i=0
	while True:
		a=connect().mem_info()
		i+=1
		paint(i,a)
	plt.ioff()
	plt.show()



if __name__ == '__main__':
	main()
