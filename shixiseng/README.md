


因为大三马上结束了，要找实习了，所以找了个实习僧网站爬一爬，看看有什么合适的工作没有<br>

1.先打开网页看一看源代码：<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/3.JPG)<br>
	发现代码是这样的，那么正则就可以写了<br>
	`>name = r'data-desc="search-职位名称">(.*?)</a>'`<br>
	其他的类似。<br>
	
2.然后试着爬取一下，发现结果是这样的:<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/img_folder/shixiseng/1.JPG)<br>
3.为什么有乱码啊，最开始我以为是在js里面，把js用fiddler4替换了，发现在网页里面字符照常显示，就判断了一下不是js里面，终于在请求页面找到了可疑的东西，如图<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/4.JPG)<br>
4.通过修改里面的字符，结果终于出现了变化，于是百度得知，这个是一种web字体，他们将字体用base64加密后上传得到字符，详细的可以百度，然后我查了很多资料尝试着解密<br>
	
5.还原字体：<br>
	将base64的字符获取<br>
	`>base64 = r'base64,(.*?)"\)}'`<br>
	`>base64_code = re.findall(base64,str(response))`<br>
	`>base_str = base64_code[0]`<br>
6.将获取到的字符用base64解码并保存到字体文件<br>
	`>base = base64.b64decode(base_str)`<br>
	`>print(base_str)`<br>
	`>with open('f.ttf','wb') as f:`<br>
	`>	f.write(base)`<br>
	`>	f.close()`<br>
7.打开字体文件看一看,用fonttools工具<br>
	`>from fontTools.ttLib import TTFont`<br>
	`>font = TTFont('f.ttf')`<br>
	`>font.saveXML('f.xml')`<br>
	`>font_list = font.getGlyphOrder()`<br>
8.这里把字体保存到xml文件，并且获得了一个list，是字体里面的编码:<br>
	这是xml的重点对象，显示了编码与字体的映射关系<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/5.JPG)
<br>9.这是字体的list列表<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/7.JPG)
0.字体解码，实习僧并没有难为我们，很简单的转换<br>
	然后实验发现'uni30'编码去掉uni变成30，转变成10进制，再变成字符<br>
	`>chr(int('30'))`<br>
	`>0`<br>
11.用正则获取xml里面的映射关系，并表示为字典:<br>
	`>codes = {}`<br>
	`>with open('f.xml','r') as f:`<br>
	`>	content = f.read()`<br>
	`>	for i in font_list:`<br>
	`>		n = i.replace('uni','')`<br>
	`>		xml_re = r'<map code="(.*)" name="'+i+'"/>'`<br>
	`>		code = re.search(xml_re,str(content)).group(1)`<br>
	`>		co = code.replace('0x','&#x')`<br>
	`>		codes[co] = chr(int(n,16))<br>
12.如图:<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/6.JPG)<br>
	
13.最后把网页中的字符替换，根据我们保存的字典里面的映射关系，一一替换显示<br>
	效果图：<br>
	![Imagetext](https://raw.githubusercontent.com/yjz1234/python/master/img_folder/shixiseng/2.JPG)<br>
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	