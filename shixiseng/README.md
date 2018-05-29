


因为大三马上结束了，要找实习了，所以找了个实习僧网站爬一爬，看看有什么合适的工作没有

*1.先打开网页看一看源代码：
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/3.JPG)
	发现代码是这样的，那么正则就可以写了
	>name = r'data-desc="search-职位名称">(.*?)</a>'
	其他的类似。
	
*2.然后试着爬取一下，发现结果是这样的:
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/1.JPG)
	>为什么有乱码啊，最开始我以为是在js里面，把js用fiddler4替换了，发现在网页里面字符照常显示，就判断了一下不是js里面，终于在请求页面找到了可疑的东西，如图
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/4.JPG)
	>通过修改里面的字符，结果终于出现了变化，于是百度得知，这个是一种web字体，他们将字体用base64加密后上传得到字符，详细的可以百度，然后我查了很多资料尝试着解密
	
*3.还原字体：
	将base64的字符获取
	>base64 = r'base64,(.*?)"\)}'
	>base64_code = re.findall(base64,str(response))
	>base_str = base64_code[0]
	将获取到的字符用base64解码并保存到字体文件
	>base = base64.b64decode(base_str)
	>print(base_str)
	>with open('f.ttf','wb') as f:
	>	f.write(base)
	>	f.close()
	打开字体文件看一看,用fonttools工具
	>from fontTools.ttLib import TTFont
	>font = TTFont('f.ttf')
	>font.saveXML('f.xml')
	>font_list = font.getGlyphOrder()
	>这里把字体保存到xml文件，并且获得了一个list，是字体里面的编码:
	这是xml的重点对象，显示了编码与字体的映射关系
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/5.JPG)
	这是字体的list列表
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/7.JPG)
	字体解码，实习僧并没有难为我们，很简单的转换
	然后实验发现'uni30'编码去掉uni变成30，转变成10进制，再变成字符
	>chr(int('30'))
	>0
	用正则获取xml里面的映射关系，并表示为字典:
	>codes = {}
	>with open('f.xml','r') as f:
	>	content = f.read()
	>	for i in font_list:
	>		n = i.replace('uni','')
	>		xml_re = r'<map code="(.*)" name="'+i+'"/>'
	>		code = re.search(xml_re,str(content)).group(1)
	>		co = code.replace('0x','&#x')
	>		codes[co] = chr(int(n,16))
	如图:
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/6.JPG)
	
*4.最后把网页中的字符替换，根据我们保存的字典里面的映射关系，一一替换显示
	效果图：
	>![Imagetext](https://github.com/yjz1234/python/shixiseng/2.JPG)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	