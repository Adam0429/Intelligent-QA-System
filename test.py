import re
import jieba.posseg as pseg
import jieba.analyse

# jieba.load_userdict(file_name) 
question_word = ['谁','何','什么','哪儿','哪里','几时','几','多少','怎','怎么','怎的','怎样','怎么样','怎么着','如何','为什么','高']
# 这里还得附上词性，不然抽取疑问词时仍然在用jieba库的词性标注
def extract_keyword(text,withWeight=False):
	tags = jieba.analyse.extract_tags(text,withWeight=withWeight)
	return tags

def question_keyword(text,question_word): 
	words = pseg.cut(text)
	wds = {}
	keywords = []
	for word,flag in words:
		wds[word] = flag
	# print(wds)
	w1= {}
	for word in wds.keys():
		if word in question_word:
			w1[word] = wds[word]
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
 
text = "荷兰人有多高"
keywords = question_keyword(text,question_word)
print(keywords)



