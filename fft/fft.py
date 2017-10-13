#coding:utf-8
import numpy as np
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import argparse
import matplotlib.pyplot as plt
import cv2

#形参命令
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

#定义一个函数，进行傅里叶变换，利用Image打开傅里叶变换后的图片，当作参数返回
def fft_():
	img = cv2.imread(args.file,0)
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)
	ma = np.log(np.abs(fshift))
	#ma = np.abs(fshift)#傅里叶变换取绝对值，因为在图片中，负数没有意义
	plt.imsave('ma.jpg',ma) #这儿在使用cv2保存的时候会出现im.load()出错
	return Image.open('ma.jpg')

#定义一个函数进行图片文本添加
def draw_(img):
	draw = ImageDraw.Draw(img)
	x,y = img.width, img.height
	if x > 1080:
		c = 50
	else:
		c = 20
	font = ImageFont.truetype('C:\Windows\Fonts\simsun.ttc',c)#设置字体
	name = input("请输入你的名字:")
	if '\u4e00' <= name<='\u9fff':#判断输入是否中文，方便计算中文大小，以便美观,当然这个数值并不是很准确，只是个人喜好
		l = len(name)
	else:
		l = len(name)/2
	draw.text((x-l*c, y-c),name,(0,0,0),font=font)#四个参数，第一个是文本位置，第二个是要设置的文本，第三个，颜色，第四个是字体
	draw = ImageDraw.Draw(img)
	img.save('201510215226.jpg')

#定义一个函数，将图片是rgba的转化成rgb
def convert(img):
	if len(img.split()) == 4:
		r,g,b,a = img.split()
		img = Image.merge('RGB', (r,g,b))
		return img
	else:
		return
if __name__ == '__main__':
	pic = fft_()
	img = convert(pic)
	draw_(img)
	
