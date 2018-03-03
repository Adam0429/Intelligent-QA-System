import re
import jieba.posseg as pseg
import jieba.analyse

# jieba.load_userdict(file_name) 

def extract_keyword(text,withWeight=False):
	tags = jieba.analyse.extract_tags(text,withWeight=withWeight)
	return tags

def answer_attr(text): 
	if '什么东西' in text or '啥' in text:	
		return '物'
	if '谁' in text or '什么人' in text:
		return '人'
	return 'dont know'	

text = "什么东西最硬"
# words = pseg.cut(text)
# for word,flag in words:
# 	print(word)
# 	print(flag)
keywords = extract_keyword(text)
print(keywords)
attr = answer_attr(text)
print(attr)

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



