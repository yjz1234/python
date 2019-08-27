#!/usr/bin/env python2
# encoding: utf-8
#@Auther     :   yjz
#@File       :   pdf_change.py
#@Time       :   2019/8/27 16:13
#@Version    :   0.1
#@Function  : 主要是简单去除水印，方便打印，具体情况具体分析，需要修改代码

import io
import os
import cv2
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader,PdfFileWriter
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas


#读取pdf文件返回pdf文件对象
def readPdf(filename):
    if os.path.exists(filename):
        reader=PdfFileReader(filename,strict=False)
        return reader
    else:
        return False


#将pdf转换成图片，供pdf转换程序读取，应该可以直接传入BMP格式的矩阵，进行生成，暂时未测试
def changeImg(reader,dir):
    page=reader.getNumPages()
    print(page)
    for i in range(0,page):
        content=reader.getPage(i)
        dst_content=PdfFileWriter()
        dst_content.addPage(content)

        pdf_bytes=io.BytesIO()
        dst_content.write(pdf_bytes)
        pdf_bytes.seek(0)

        img=Image(file=pdf_bytes,resolution=300)
        img.format='BMP'
        img.compression_quality = 90
        img.background_color = Color("white")
        img_path = dir+'%d.BMP'%i
        img.save(filename=img_path)
        img.destroy()

#图片根据需求剪裁，二值化去水印
def imageReshape(dir,page):
    for i in range(0,page):
        #此处21以上的才有水印
        if(i>21 or i==0):
            img = cv2.imread(dir + '%d.BMP' % i,cv2.IMREAD_UNCHANGED)
            #二值化，水印的原理是增加一个透明度，使用掩码生成图片
            # 我使用的pdf是将有用的信息作为掩码使用的，所以需要将a通道分离出来，其他通道自行参考分离
            b, g, r, a = cv2.split(img)
            #掩码二值化，将灰色部分的水印去除
            ret, img = cv2.threshold(a, 127, 255, cv2.THRESH_BINARY_INV)
            shape = a.shape
            h = shape[0]
            w=shape[1]
        else:
            img = cv2.imread(dir + '%d.BMP' % i)
            shape = img.shape
            h = shape[0]
            w = shape[1]
        #裁剪图片去除页眉页尾的网址
        cv2.imwrite(dir + '%d.BMP' % i, img[int(h*0.1):int(h-h*0.05), int(w*w*0.075/h):shape[1]-int(w*w*0.075/h)])

#将图片转换成pdf，长宽比采用portrait模式
def changePdf(dir,page):
    h,w=portrait(A4)
    c = canvas.Canvas("my.pdf", pagesize=(h,w))
    for i in range(0,page):
        c.drawImage(os.getcwd()+"\%d.BMP"%i,0,0,h,w)
        c.showPage()
    c.save()




def main():
    filename=input('转换的pdf文件(绝对路径):')
    dir=input('保存的文件夹:')
    reader=readPdf(filename)
    if reader:
        changeImg(reader,dir)
        imageReshape(dir,reader.getNumPages())
        changePdf(dir,reader.getNumPages())

if __name__=='__main__':
    main()