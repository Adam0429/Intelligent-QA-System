from flask import Flask,abort,request,redirect,render_template,jsonify  
from flask_script import Manager
# from flask_bootstrap import Bootstrap
# from wtforms import StringField,SubmitField
# from wtforms.validators import Required
import jieba.posseg as pseg
import codecs
import pymysql
from tqdm import tqdm
from gensim import corpora
from gensim.summarization import bm25
from gensim.summarization.bm25 import get_bm25_weights
import os
import re
import pickle
import jieba
from jieba import analyse
import pymysql

app = Flask('my web')
app.config['SECRET_KEY'] = '1234231'
jieba.load_userdict('dict.txt') 

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

def del_div(strings):
	dr = re.compile(r'<div[^>]+>',re.S)
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

def find_a(strings):
	regex=re.compile('<a.*>')
	string = regex.findall(strings)
	if len(string) != 0:
		return string[0]
	else:
		return ''
def f1(result):
	best_answer = [result[0]]
	min_word = len(result[0][0].split('-'))
	# print(result)
	for r in result:
		length = len(r[0].split('-'))
		# print(r)
		# print(length)
		# 先取出字条数最少的，再在其中找到长度最短的
		# 改成计算文本相似度
		if length < min_word:
			min_word = length
			best_answer = [r]
		if length == min_word:
			best_answer.append(r)
	best = best_answer[0]
	num = len(best_answer[0])
	for b in best_answer:
		length = len(b[0])
		if length < num:
			best = b
	return best 

def andsearch(keywords,attr,attr2):
	first = True
	sql = 'select ' + attr + ' from QA where '
	for w in keywords:
		if first:   
			sql = sql + attr2 +' like "%' + w + '%" '
			first = False
		else:
			sql = sql + 'and ' + attr2 + ' like "%' + w + '%" '
	return sql

def orsearch(keywords,attr,attr2):
	first = True
	sql = 'select ' + attr + ' from QA where '
	for w in keywords:
		if first:   
			sql = sql + attr2 + ' like "%' + w + '%" '
			first = False
		else:
			sql = sql + 'or ' + attr2 +' like "%' + w + '%" '
	return sql

def tokenization(text):
	stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
	result = []
	words = pseg.cut(text)
	for word, flag in words:
		if flag not in stop_flag:
			result.append(word)
	return result

# def feedback(desc,title,keywords):
# 	db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
# 	cursor = db.cursor()
# 	cursor.execute('select descs from QA where normal_question == "'+title'"')
# 	result = cursor.fetchall()[0]
# 	print(result)
# 	words = result.split(' ')

# 	cursor.execute("update QA set descs='"+keywords+"' where normal_question='"+keywords+"'")
	# corpus = []
	# descs = []
	# cursor.execute('select answer from QA')
	# for c in cursor.fetchall():
	# 	corpus.append(c[0])
	# cursor.execute('select descs from QA')
	# for c in cursor.fetchall():
	# 	descs.append(c[0])
	# data = []
	# data.append(corpus)
	# data.append(descs)
	# output = open('bm25.model', 'wb')
	# pickle.dump(data,output)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
	return render_template('chat.html')

@app.route('/getanswer', methods=['GET', 'POST'])
def getanswer():
	question = request.args['question']
	query = question
	q2 = query.upper()
	q3 = query.lower()
	keywords = analyse.extract_tags(query, withWeight=False)
	# allowPOS=['ns','n','vn','v','nr']
	# 处理大小写不能分出关键词的问题,分词区分大小写,而数据库查询不区分
	# keywords = ['帮助中心','产品术语-驱动']
	print(keywords)
	# 如没有关键词,就需要分词将所有词做关键词
	if len(keywords) == 0:
		keywords = jieba.cut(query,cut_all = True)
		keywords = '/'.join(keywords)
		keywords.split('/')

	sql = andsearch(keywords,'answer,descs','descs')
	sql2 = orsearch(keywords,'answer,descs','descs')
	print(sql2)

	db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.execute(sql2)
	result2 = cursor.fetchall()
	if len(result) == 0:
		if result2 == 0:
			result == None
		else:
			result = result2
	
	descs = []
	corpus = []

	if len(result) == 1:
		sql = 'select normal_question,answer from QA where descs="' + result[0][1] + '"'
		cursor.execute(sql)
		result = cursor.fetchall()
		title = result[0][0]
		answer = '<h2>' + title + '</h2>' + result[0][1]
		# 当答案中只有一个<a>时,需要加上'链接'让其显示
		if del_tag(answer) == title:
			answer = '<h2>' + title + '</h2>' + find_a(answer) + '链接'
		else:
			answer = del_div(answer)	
		answer = answer.replace('</div>','')
		answer = '<div>' + answer + '</div>'
		answer = answer.replace(']','')

		print(answer)
		return answer

	elif len(result) != 0:
		for r in tqdm(result):
			text = del_tag(r[1])			
			#index为1是用标签搜索，改为0是用答案搜
			terms = tokenization(text)
			corpus.append(terms)
			descs.append(r[1])

	
	# 如果标题都没出现,去答案里找
	else:
		# corpus = []
		# descs = []
		# cursor.execute('select answer from QA')
		# for c in cursor.fetchall():
		# 	corpus.append(c[0])
		# cursor.execute('select descs from QA')
		# for c in cursor.fetchall():
		# 	descs.append(c[0])
		# data = []
		# data.append(corpus)
		# data.append(descs)
		# output = open('bm25.model', 'wb')
		# pickle.dump(data,output)
		f = open("bm25.model","rb")
		bin_data = f.read()
		data = pickle.loads(bin_data)
		corpus = data[0]
		descs = data[1]


	# for d in descs:
	# 	print(d)

	bm25Model = bm25.BM25(corpus)
	average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())


	scores = bm25Model.get_scores(keywords,average_idf)
	_scores = list(set(scores))
	_scores.sort(reverse=True)

	# idx = scores.index(max(scores))
	# print(idx)
	# print(corpus[idx])
	# print(descs[idx])
	# print(scores)
	answer = ''
	url = []
	titles = []
	for s in _scores[:3]:
		print(s)
		idx = scores.index(s)
		cursor.execute('select url from QA where descs = "'+descs[idx]+'"') 
		url.append(cursor.fetchall()[0][0])

	url = list(set(url))

	if len(url) == 1:
		print(url)
		cursor.execute('select descs from QA where url = "'+url[0]+'"') 
		for c in cursor.fetchall():
			titles.append(c[0])

	else:
		for s in _scores[:3]:
			idx = scores.index(s)
			titles.append(descs[idx])
			print(descs[idx])
			print(scores[idx])

	totalanswer = ''
	for title in tqdm(titles):
		# print(title)
		sql = 'select normal_question,answer from QA where descs="' + title + '"'
		cursor.execute(sql)
		result = cursor.fetchall()
		title = result[0][0]
		answer = '<h2>' + title + '</h2>' + result[0][1]
		# print(cursor.fetchone())
		if del_tag(answer) == title:
			answer = '<h2>' + title + '</h2>' + find_a(answer) + '链接'
		totalanswer = totalanswer + answer + '<split>'

	totalanswer = del_div(totalanswer)
	totalanswer = totalanswer.replace('</div>','')
	totalanswer = totalanswer.replace(']','')
	#totalanswer = '<div>' + totalanswer + '</div>' 
	print(totalanswer)
	return totalanswer
	# 取前3个排序,如来自同一网页则返回网页下所有内容,不是则都返回

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)


