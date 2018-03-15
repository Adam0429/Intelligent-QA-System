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
	data = {}
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
		ele = soup.select('.topictitle1')
		ele = del_tag(ele)
		if len(ele) == 1:
			data['title'] = ele[0]
			t.append(data['title'])
		else:
			data['title'] = 'null'
		data['desc'] = t
		details = soup.select('.help-details')
		soup2 = BeautifulSoup(str(details),'lxml')
		p = soup2.select('p')	
		p = del_tag(p)
		string = ''
		for i in p:
			string = string + i
		data['content'] = string
		print(data)
