# -*- coding: utf-8 -*-
#作者：Wang Feihong
#python 版本：3.6
#更新时间 2018/3/18
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
		h1s = soup.select('h1')
		t = del_tag(elements)
		if "上一篇" in text:
			t.remove(t[len(t)-1])
		if "下一篇" in text:
			t.remove(t[len(t)-1])
		ele = soup.select('.topictitle1')
		title = del_tag(ele)
		if len(title) == 1:
			data['title'] = title[0]
			t.append(data['title'])
		else:
			data['title'] = 'null'
		data['desc'] = t

		details = soup.select('.help-details')
		if len(details) == 0:
			details = soup.select('div[id^="body"]') 
		if len(details) == 0:
			details = soup.select('.beg-text')
		if len(details) == 0:	
			details = soup.select('.periods')
		if len(details) == 0:	
			details = soup.select('.helpContent')	
		if len(details) == 0:	
			details = soup.select('.record-content')
		if len(details) == 0:
			continue
		# 正常是所有页面都有一个div储存问答信息,类名不一定是什么，大概就上面几种

		qas = []
		soup2 = BeautifulSoup(str(details),'lxml')
		sections = soup2.select('.section')	
		# 分两类,有无section的情况
		# print(len(sections))
		string1 = str(details).split('<div')[2]
		data['intro'] = (del_tag(['<'+string1]))
		# 这是总标题的解释，位于总标题的下端
		if len(sections) > 0:
			# 每个<h4>和<p><table>等一些列作为答案的标签一一对应
			for section in sections:
				soup3 = BeautifulSoup(str(section),'lxml')
				h4s = soup3.select('h4')
				if len(h4s) != 0 :
					for h4 in h4s:
						answer = str(section).split(str(h4))[1]
						answer = del_tag([answer])
						h4 = del_tag([h4])
						qa = {'question':h4[0],'answer':answer}
						qas.append(qa)
		data['qa'] = qas
		print(data)

		# else: 

