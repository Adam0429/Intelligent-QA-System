import re
import jieba.posseg as pseg
import jieba.analyse

# jieba.load_userdict(file_name) 
# question_word = ['谁','何','什么','哪儿','哪里','几时','几','多少','怎','怎么','怎的','怎样','怎么样','怎么着','如何','为什么','高']

# 这里还得附上词性，不然抽取疑问词时仍然在用jieba库的词性标注
def extract_keyword(text,withWeight=False):
	tags = jieba.analyse.extract_tags(text,withWeight=withWeight)
	return tags

def question_keyword(text,question_word): 
	words = pseg.cut(text)
	wds = {}
	w = []
	keywords = []
	
	for word,flag in words:
		w.append(word)
		wds[word] = flag
	print(wds)
	if '多少' in w:		#判断疑问词的顺序也有讲究,通常出现多少就可以判断为多少是疑问词.这里因为多少是作为量词出现,所以加一步判断
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
	# for word in wds.keys():'
			# if word in question_word:
		# 	w1[word] = wds[word]
		# print(w1)
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

text = "这个班有多少人"
keywords = question_keyword(text,[])
print(keywords)
questiontype = question_type(keywords)
print(questiontype)



# words = pseg.cut("什么哪里?")
# dict = {}
# for word,flag in words:
# 	print(word)
# 	print(flag)
# 	dict[word] = flag
# # print(dict)
# keys = dict.keys()
# r = []
# for key in keys:
# 	if dict[key] == 'r':
# 		r.append(key)
# print(r)



