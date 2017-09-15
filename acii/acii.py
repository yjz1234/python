#coding:utf-8

from PIL import Image
import argparse
#形参命令
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

#形参命令的文件
imgpath = args.file

#字符画列表的像素，从高到低由list中字符顺序替代
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

#定义一个函数，灰度值转换公式
def select_acii_char(r,g,b):
	gray = int((19595 * r + 38469 * g +7472 *b) >> 16)
	unit = 256.0/len(ascii_char)
	return ascii_char[int(gray/unit)]
	
#定义一个函数，输出字符画
def output(imgpath,height,width):
	im =Image.open(imgpath)
	
	#获取图片的高度
	height = im.height
	
	#获取图片的宽度
	width = im.width
	
	im = im.resize((width, height), Image.NEAREST)
	txt = ""

	#进行字符画的绘制
	for x in range(height):
		for i in range(width):
			txt += select_acii_char(*im.getpixel((i,x))[:3])
		txt +='\n'
	return txt 

#定义一个函数，保存字符画到img.txt文件中	
def save(txt):
	with open('img.txt', 'w+') as f:
		f.write(txt)
	
	
if __name__ == '__main__':
	print(output(imgpath,40,30))
	save(output(imgpath,40,30))