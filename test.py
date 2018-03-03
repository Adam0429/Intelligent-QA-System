import jieba.posseg as pseg
#jieba.load_userdict(file_name) 
words = pseg.cut("什么哪里?")
dict = {}
for word,flag in words:
	print(word)
	print(flag)
	dict[word] = flag
# print(dict)
keys = dict.keys()
r = []
for key in keys:
	if dict[key] == 'r':
		r.append(key)
print(r)
