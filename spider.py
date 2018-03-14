import re
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

def del_tag(strings):
	dr = re.compile(r'<[^>]+>',re.S)
	strs = []
	for string in strings:
		string = str(string)
		s = dr.sub('',string)
		strs.append(s)
	return strs

path = '/home/wangfeihong/桌面/support.huaweicloud.com/'

files = os.listdir(path)

for file in tqdm(files):
	if not 'developer' in file:
		f = open(path + file,mode = 'r')
		text = f.read()
		print(file)
		soup = BeautifulSoup(text,'lxml')
		elements = soup.select('.help-link')
		t = del_tag(elements)
		if "上一篇" in text:
			t.remove(t[len(t)-1])
		if "下一篇" in text:
			t.remove(t[len(t)-1])
		eles = soup.select('.topictitle1')
		eles = del_tag(eles)
		details = soup.select('.help-details')
		soup2 = BeautifulSoup(str(details),'lxml')
		p = soup2.select('p')	
		p = del_tag(p)
		content = ''
		for i in p:
			content = content + i
		print(eles + t + [content])


	# print(elements)
	# if '华为云帮助中心' not in t:
	# 	print(t)

