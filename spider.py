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
	if type(strings) == type([]): 
		strs = []
		for string in strings:
			string = str(string)
			s = dr.sub('',string)
			strs.append(s)
		return strs
	else:
		strings= str(strings)
		s = dr.sub('',strings)
		return s


path = '/home/wangfeihong/桌面/support.huaweicloud.com/'

files = os.listdir(path)
# txt = open('1.txt','w+')
for file in tqdm(files):
	data = {}	
	f = open(path + file,mode = 'r')
	text = f.read()
	# print(file)
	if not 'developer' in file:
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
		soup2 = BeautifulSoup(text,'lxml')
		if len(title) == 1:
			data['title'] = title[0]
			t.append(data['title'])
		else:
			data['title'] = 'null'
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
			details = soup.select('.help-main')
		if len(details) == 0:
			continue
		# 正常是所有页面都有一个div储存问答信息,类名不一定是什么，大概就上面几种

		soup = BeautifulSoup(str(details),'lxml')
		soup2 = BeautifulSoup(text,'lxml')
		descs = soup2.select('.crumbs')
		# soup3 = BeautifulSoup(str(descs),'lxml')
		desc = []
		qas = {}

		if len(descs) == 0:
			descs = soup2.select('.position')
		if len(descs) != 0:
			for c in descs[0].children:
				if not c.isspace:
					desc.append(del_tag(c))
			data['desc'] = desc
		if 'desc' not in data:
			data['desc'] = ['null'] 

		h1 = soup.h1
		# print(data['desc'])

		if h1 is None:
		# some index and faq pages

			if len(soup2.select('.beg-title')) == 0:
				data['title'] = 'null'
			else: 
				data['title'] = del_tag(soup2.select('.beg-title')[0])
			if ps[1:] != []:
				if len(data['desc']) == 0:
					qas[data['title']] = del_tag(ps[1:])
				else:
					qas[data['desc'][len(data['desc'])-1]] = del_tag(ps[1:])
			if len(data['desc']) == 0:
				data['desc'] = data['title']

			h5s = soup.select('h5')
			h4s = soup.select('h4')
			h3s = soup.select('h3')
			h1s = soup.select('h1')
			hs = h1s + h3s + h4s + h5s
			if len(hs) > 0:
				for h in hs:
					for s in h.next_siblings:
						if not s.isspace:
							if del_tag(h) not in qas.keys():
								qas[del_tag(h)] = del_tag(s)
			# txt.writelines("-".join(str(data['desc'])))
			# txt.writelines('\n')
			data['qas'] = qas			
			# print(data['qas'])
		else:
			ps = soup.select('p')
			h5s = soup.select('h5')
			h4s = soup.select('h4')
			h3s = soup.select('h3')
			h1s = soup.select('h1')
			hs = h1s + h3s + h4s + h5s
			qas = {}
			if len(hs) > 0:
				for h in hs:
					for s in h.next_siblings:
						if not s.isspace:
							if del_tag(h) not in qas.keys():	
								qas[del_tag(h)] = del_tag(s)
			# dls = soup.select('dl')
			# if len(dls) > 0:
			# 	for dl in dls:
			# 		for s in dl.next_siblings:
			# 			if not s.isspace:
			# 				soup2 = BeautifulSoup(str(dl),'lxml')
			# 				dts = soup2.dt
			# 				dds = soup2.select('dd')
			# 				dds = del_tag(dds)
			# 				qas.append({'question':del_tag(dts),'answer':del_tag(s)}) 
			data['qas'] = qas
			# for key,value in qas.items():
			# 	print(key)
			# 	print('========================================')
			# 	print(value)
			# txt.writelines("".join(str(data['desc'])))
			# txt.writelines('\n')

	# developer
	else:
		soup = BeautifulSoup(text,'lxml')
		details = soup.select('#content')
		soup = BeautifulSoup(str(details),'lxml')
		descs = soup.select('.crumbs')
		titles = soup.select('span')
		h1 = soup.h1
		qas = {}

		# 找到所有h3作为问题，再找他的兄弟节点作为答案
		if len(descs) == 0:
			descs = soup.select('.position')
		if len(descs) != 0:
			for c in descs[0].children:
				if not c.isspace:
					desc.append(del_tag(c))
			data['desc'] = desc
		# if h1 is None:
		h5s = soup.select('h5')
		h4s = soup.select('h4')
		h3s = soup.select('h3')
		h1s = soup.select('h1')
		hs = h1s + h3s + h4s + h5s
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# 想法是找到每个h4的位置,每两个h4的之间的内容就是第一个h4的答案,原先找h4的子节点方法不可用，因为网页写得太乱,div有些包括答案和内容，有些不包括
		if len(hs) > 0:
			for h in hs:
				for s in h.next_siblings:
					if not s.isspace:
						qas[del_tag(h)] = del_tag(s)
		dls = soup.select('dl')
		if len(dls) > 0:
			for dl in dls:
				for s in dl.next_siblings:
					if not s.isspace:
						soup2 = BeautifulSoup(str(dl),'lxml')
						dts = soup2.dt
						dds = soup2.select('dd')
						dds = del_tag(dds)
						qas[del_tag(dts)] = del_tag(s) 
		data['qas'] = qas						
		data['title'] = del_tag(soup.select('.poster-caption'))[0]
			# if len(data['desc']) == 0:
		data['desc'] = [data['title']]
			# print(data['qas'])
			# txt.writelines("-".join(str(data['desc'])))
			# txt.writelines('\n')
	print(file)
	print(data['qas'])
