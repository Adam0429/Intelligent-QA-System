from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser
import codecs
from tqdm import tqdm
import time
import os
import re
from bs4 import BeautifulSoup
import pymysql

db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
idx = 1
_postagger = Postagger()  
_postagger.load('/home/wangfeihong/桌面/ltp_data/pos.model')  
_segmentor = Segmentor()  # 初始化实例
_segmentor.load('/home/wangfeihong/桌面/ltp_data/cws.model')  # 加载模型

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

def filter(List):
    useless_labels = ['简介','帮助中心','概览','产品简介','快速入门','FAQ','用户指南']
    nList = list()
    for label in List:
        if label not in useless_labels:
            nList.append(label)
#    for label in nList:
#        print(label + ' ', end = '')
#    print()
    return nList;

def segmentor(_segmentor,sentence=''):
    words = _segmentor.segment(sentence)  # 分词
    # 可以转换成List 输出
    words_list = list(words)
    # _segmentor.release()  # 释放模型
    return words_list

#词性标注  
def posttagger(_posttagger,words):  
    
    posttags=_posttagger.postag(words)  #词性标注  
    postags = list(posttags)  
    # _posttagger.release() #释放模型  
    #print type(postags)  
    return postags

#生成问句
def generator(_segmentor,_postagger,List):
    labels = List
    useful_labels = filter(labels)
    #找到最后一个标签
    last_label = segmentor(_segmentor,useful_labels[-1])
    #记录最后一个标签的所有词性
    last_label_postages = posttagger(_postagger,last_label)
    #动词做定语
    adjVlist = ["使用限制","计费方式","操作指南","准备工作","使用限制"]

    #假如只有一个有用标签或最后一个标签包含简介
    if (
        len(useful_labels) == 1 or
        useful_labels[-1].find('简介') != -1
    ):
        return '什么是' + useful_labels[0] + '?'

    #假如最后一个标签的开头是“什么”或介词如"与"，则不需要生成问题
    elif (
        last_label[0] == '什么' or
        last_label[0] == '怎么' or
        last_label[0] == '如何'
    ):
        str = ''
        return str.join(last_label) + '？'

    #假如最后一个标签就是概述或者产品概述
    elif (
        useful_labels[-1] == '概述' or
        useful_labels[-1] == '产品概述'
    ):
        return useful_labels[0] +'的' + useful_labels[-2] + '？'

    #假如最后一个标签在例外情况（动词开头）之中
    elif useful_labels[-1] in adjVlist:
        return useful_labels[0] +'的' + useful_labels[-1] + '有哪些？'

    #假如最后一个标签的最后一个词为管理
    elif last_label[-1] == '管理':
        str = ''
        return '怎么管理' + useful_labels[0] + '的' + str.join(last_label[:-1])

    # 假如最后一个标签的最后一个词为接口
    elif (
        last_label[-1] == '接口' or
        last_label[-1] == '指南'
    ):
        str = ''
        return useful_labels[0] + '的' + str.join(last_label) + '有哪些？'

    #假如最后一个标签是"购买指南"
    elif useful_labels[-1] == '购买指南':
        return '怎么购买' + useful_labels[0] + '？'

    #假如最后一个标签的开头是动词，则用“怎么... ...”生成问句
    elif last_label_postages[0] is 'v':
        #假如最后一个标签只有一个动词，例如“入门”
        if len(last_label_postages) == 1:
            return '怎么' + last_label[0] + useful_labels[0] + '？'
        else:
            #假如只有一个动词加其他词，例如“管理集群”
            if (
                '和' not in last_label and
                '或' not in last_label and
                '并' not in last_label and
                '与' not in last_label
            ):
                str = ''
                return '怎么' + last_label.pop(0) + useful_labels[0] + '的' + str.join(last_label) + '？'
            #假如超过一个动词，例如“访问和使用DWS”
            else:
                last_label_postages.reverse()
                index_of_last_v = len(last_label_postages) - last_label_postages.index('v')
                last_label_postages.reverse()
                str = ''
                #假如只有动词
                if last_label_postages[-1] is 'v':
                    return '怎么' + str.join(last_label[:index_of_last_v]) + useful_labels[0] + '？'
                #假如有其他词
                else:
                    return '怎么' + str.join(last_label[:index_of_last_v]) + useful_labels[0] + '的' + str.join(last_label[index_of_last_v:]) + '？'
#假如最后一个标签为"与... ..."，使用第一个标签和最后一个标签形成问句
    elif last_label[0] == '与':
        return useful_labels[0] + useful_labels[-1] + '？'

    #假如最后一个标签的开头是其他词汇，则用“... ...有哪些”生成问句
    else:
        str = ''
        return useful_labels[0] + '的' + str.join(last_label) + '有哪些？'

path = '/home/wangfeihong/桌面/support.huaweicloud.com/'
files = os.listdir(path)
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
		soup2 = BeautifulSoup(text,'lxml')
		details = soup.select('.help-details')
		if len(details) == 0:
			details = soup.select('div[id^="body"]') 
		if len(details) == 0:
			details = soup.select('.beg-text')
		if len(details) == 0:	
			details = soup.select('.periods')
		if len(details) == 0:
			details = soup.select('.help-main')
		if len(details) == 0:	
			details = soup.select('.helpContent')	
		if len(details) == 0:	
			details = soup.select('.record-content')
		if len(details) == 0:
			details = soup.select('.content-block')
		if len(details) == 0:
			# print('!!!!!:'+file)
			continue
		# 正常是所有页面都有一个div储存问答信息,类名不一定是什么，大概就上面几种
		details = str(details)
		soup = BeautifulSoup(details,'lxml')
		soup2 = BeautifulSoup(text,'lxml')
		descs = soup2.select('.crumbs')
		# soup3 = BeautifulSoup(str(descs),'lxml')
		desc = []

		if len(descs) == 0:
			descs = soup2.select('.position')
		if len(descs) != 0:
			for c in descs[0].children:
				if not c.isspace:
					desc.append(del_tag(c))
			data['desc'] = desc
		if 'desc' not in data:
			data['desc'] = ['null'] 

		h1 = soup2.h1
		# print(data['desc'])
		h5s = soup.select('h5')
		h4s = soup.select('h4')
		h3s = soup.select('h3')
		h2s = soup.select('h2')
		h1s = soup.select('h1')
		hs = h1s + h2s + h3s + h4s + h5s
		questions = {}
		qas = {}	
		for h in hs:
			index = details.find(str(h))
			questions[h] = index

		questions = sorted(questions.items(),key=lambda abs:abs[1])# tuple
		#还有种没标题的
		try:	
			if len(hs) == 0:
				question = data['desc'][len(data['desc'])-1]
				answer = details.split(str(descs[0]))
				# print(answer[len(answer)-1])
				qas[del_tag(question)] = answer[len(answer)-1]
			if len(questions) == 1:
				answer = details.split(str(h))[1]
				answer = answer.replace('\n','')
				answer = answer.replace("'","''")
				if '父主题' in answer:
					answer = answer.split('父主题')[0]
				qas[del_tag(questions[0][0])] = answer
			else:
				for i in range(len(questions)-1):
					# print(questions[i][0])
					# print(questions[i+1][0])
					content = details.split(str(questions[i][0]))[1]
					content = content.split(str(questions[i+1][0]))[0] 
					answer = content				
					if '父主题' in answer:
						answer = answer.split('父主题')[0]
					qas[del_tag(questions[i][0])] = answer
		except:
			print(file+'=============')
		data['url'] = file
		data['qas'] = qas

	# developer
	else:
		soup = BeautifulSoup(text,'lxml')
		details = str(soup.select('#content'))
		soup = BeautifulSoup(str(details),'lxml')
		descs = soup.select('.crumbs')
		titles = soup.select('span')
		h1 = soup.h1
		if len(descs) == 0:
			descs = soup.select('.position')
		if len(descs) != 0:
			for c in descs[0].children:
				if not c.isspace:
					desc.append(del_tag(c))
			data['desc'] = desc
		else:
			data['desc'] = [del_tag(str(soup.h1))]
		# if h1 is None:
		h5s = soup.select('h5')
		h4s = soup.select('h4')
		h3s = soup.select('h3')
		h2s = soup.select('h2')
		h1s = soup.select('h1')
		hs = h1s + h2s + h3s + h4s + h5s
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# 想法是找到每个h4的位置,每两个h4的之间的内容就是第一个h4的答案,原先找h4的子节点方法不可用，因为网页写得太乱,div有些包括答案和内容，有些不包括
		# 如果小标题都没有，直接拿h1做问题，剩下的都是答案		
		qas = {}
		questions = {}	
		for h in hs:
			index = details.find(str(h))
			questions[h] = index
		questions = sorted(questions.items(),key=lambda abs:abs[1])# tuple
		# print(questions)
		try:
			if len(hs) == 0:
				question = data['desc'][len(data['desc'])-1]
				answer = details.split(str(descs[0]))
				# print(answer[len(answer)-1])
				qas[del_tag(question)] = answer[len(answer)-1]
			if len(questions) == 1:
				answer = details.split(str(h))[1]
				
				if '父主题' in answer:
					answer = answer.split('父主题')[0]
				qas[del_tag(questions[0][0])] = answer
			else:
				for i in range(len(questions)-1):
					# print(questions[i][0])
					# print(questions[i+1][0])
					content = details.split(str(questions[i][0]))[1]
					content = content.split(str(questions[i+1][0]))[0] 
					answer = content
					answer = answer.replace('\n','')
					answer = answer.replace("'","''")
					if '父主题' in answer:
						answer = answer.split('父主题')[0]
					qas[del_tag(questions[i][0])] = answer
		except:
			continue
			print('file'+'=====================')
		# ------------------------------
		data['url'] = file
		data['qas'] = qas

	# print(generator(_segmentor,_postagger,data['desc']))
	for question,answer in data['qas'].items():
		idx = idx + 1
		dd = []
		for d in data['desc']:
			if d != data['desc'][len(data['desc'])-1]:
				dd.append(d)

		dd.append(question)
		d = '-'.join(dd)
		answer = answer.replace('\n','')
		answer = answer.replace("'",'"')
		answer = answer.replace(';','')
		answer = answer.replace('”','"')
		answer = answer.replace('“','"')
		# some limit signals in sql 
		try:
			sql = 'insert into QA values(' + str(idx) + ',"' + question +'",' + '"null"' + ",'" + data['url'] + "','" + answer + "','" + d + "'" + ')'
		except:
			answer = del_tag(answer) 
			# some limit signals in sql 
			sql = 'insert into QA values(' + str(idx) + ',"' + question +'",' + '"null"' + ",'" + data['url'] + "','" + answer + "','" + d + "'" + ')' 
		print(sql)
		cursor.execute(sql)
		db.commit()
