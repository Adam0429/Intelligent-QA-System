import pymysql
import re
import jieba
from jieba import analyse
import jieba.posseg as pseg

jieba.load_userdict('dict.txt') 
# question_word = ['谁','何','什么','哪儿','哪里','几时','几','多少','怎','怎么','怎的','怎样','怎么样','怎么着','如何','为什么','高']

# 这里还得附上词性，不然抽取疑问词时仍然在用jieba库的词性标注
def question_keyword(text,question_word): 
	words = pseg.cut(text)
	wds = {}
	w = []
	keywords = []
	
	for word,flag in words:
		w.append(word)
		wds[word] = flag
	print(wds)
	if '多少' in wds.keys():
		return ['多少']
	if '什么' in w:
		index = w.index('什么')
		if index == len(w) - 1:
			pass
		else:
			n = w[index+1]
			if wds[n] == 'n':
				return [n]
	w1 = {}
	w1 = wds
	# for word in wds.keys():
	# 	if word in question_word:
	# 		w1[word] = wds[word]
	# 	print(w1)
	if 'a' in w1.values() and 'r' not in w1.values():
		for word in w1.keys():
			if w1[word] == 'a':
				keywords.append(word)
	else:		 
		for word in w1.keys():
			if w1[word] == 'r':
				keywords.append(word)
	return keywords
 
def question_type(text):
	if list(set(text).intersection(set(['何处','何地','哪儿','哪里','那儿','哪']))):
		return ('地点')
	if list(set(text).intersection(set(['何时','时候','哪天','哪年','月']))):
		return ('时间')
	if list(set(text).intersection(set(['人','谁']))):
		return ('人物')
	if list(set(text).intersection(set(['多少']))):
		return ('数字')
	if list(set(text).intersection(set(['为什么','为啥','什么样','什么意思']))):
		return ('描述')
	    # 实体 

text = input('input:')
# questionwords = question_keyword(text,[])
# # print(questionwords)
# questiontype = question_type(questionwords)
# # print(questiontype)
keywords = analyse.extract_tags(text,topK=20, withWeight=True,allowPOS=['ns','n','vn','v','nr','eng'])

db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
print(keywords)
first = True
sql = 'select descs from QA where '
for w in keywords:
	if first: 	
		sql = sql + 'descs like "%' + w + '%" '
		first = False
	else:
		sql = sql + 'and descs like "%' + w + '%" '
print(sql)
cursor.execute(sql)
result = cursor.fetchall()
print(len(result))