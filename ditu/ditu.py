#!/usr/bin/env  
#-*- coding:utf-8 -*-  
''''' 
利用高德地图api实现经纬度与地址的批量转换 
'''  
import requests  
import pandas as pd

ss = pd.read_excel('ditu.xlsx',names=['A','B'])

a=[]
for i in ss['A']:
	a.append(str(i))
b=[]
for x in ss['B']:
	b.append(x)
locations=[]
for c in range(0,300):
	locations.append(str(a[c])+','+str(b[c]))
	
for y in locations:
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	url = 'http://restapi.amap.com/v3/geocode/regeo?output=xml&location='+str(y)+'&key=******&radius=1000&extensions=all'
	response=requests.get(url=url,headers=headers)
	print(response.content)

