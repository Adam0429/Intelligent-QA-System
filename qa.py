import pymysql
import re
import jieba
from jieba import analyse
import jieba.posseg as pseg

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

def andsearch(keywords):
	first = True
	sql = 'select descs from QA where '
	for w in keywords:
		if first: 	
			sql = sql + 'descs like "%' + w + '%" '
			first = False
		else:
			sql = sql + 'and descs like "%' + w + '%" '
	return sql

def orsearch(keywords):
	first = True
	sql = 'select descs from QA where '
	for w in keywords:
		if first: 	
			sql = sql + 'descs like "%' + w + '%" '
			first = False
		else:
			sql = sql + 'or descs like "%' + w + '%" '
	return sql

jieba.load_userdict('dict.txt') 

text = input('input:')
keywords = analyse.extract_tags(text,topK=20, withWeight=False,allowPOS=['ns','n','vn','v','nr','eng'])
print(keywords)
db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
sql = andsearch(keywords)
print(sql)
cursor.execute(sql)
result = cursor.fetchall()
print(result)
# 需要一种算法：不相关的词会影响相似度
# if len(result) > 1:
# 	desc = f1(result)[0]
# 	sql = 'select answer from QA where descs = "'+f1(result)[0]+'"'
# 	print(sql)
# elif len(result) == 0:
# 	sql = orsearch(keywords)
# 	cursor.execute(sql)
# 	result = cursor.fetchall()
# 	if len(result) == 0:
# 		print('no result')
