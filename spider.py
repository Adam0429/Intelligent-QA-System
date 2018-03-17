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
		# print(file)
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
		if len(details) == 0:
			details = soup.select('div[id^="body"]') 
		if len(details) == 0:
			print(file)
		# 正常是所有页面都有这个div，如果没有要去找以body开头的
		# soup2 = BeautifulSoup(str(details),'lxml')
		# p = soup2.select('p')	
		# p = del_tag(p)
		# sections = []
		# divs = soup2.select('div[id^="body"]') 
		# # 理想中是每个div里有一个h4作为主题,but有8个超过1个h4,要分情况处理
		# print(len(divs))
		# if len(divs) == 0:
		# 	print(file)
		# 	divs = soup2.select('div[id^="body"]')
		# 	print(del_tag(divs))
		# break
		# sections = {}
		# divs = del_tag(divs)
		# for div in divs:
		# 	soup3 = BeautifulSoup(str(div),'lxml')
		# 	h4s = soup3.select('h4')
		# 	h4s = del_tag(h4s)

		# 	lis = soup3.select('li')
		# 	# lis = del_tag(lis)
		# 	soup4 = BeautifulSoup(str(lis),'lxml')  
		# 	li_as = soup4.select('p')
		# 	li_as = del_tag(li_as)
			# for li_a in li_as:
			# 	print(li_a)
		# for div in divs:
		# 	print('----------')
		# 	print(div)
		# break
		# string = ''
		# for i in p:
		# 	string = string + i
		# data['content'] = string
		# print(details)




