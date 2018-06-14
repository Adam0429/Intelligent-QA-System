import random
words = open('words.txt','r',encoding='UTF-8')
model = open('model.txt','r',encoding='UTF-8')
data = open('data.txt','w',encoding='UTF-8')
words_lines = words.readlines()
data_lines = model.readlines()
newlines = []
for line in words_lines:
	newlines.append(line[:2])
i = 0
while i < 10:
	for line in data_lines:
		question = line.strip()
		words = random.sample(newlines,10)
		templist = question.split()
		tag = templist[0]
		for word in words:	
			question = templist[1].replace('*',word)
			tempStr = tag + '\t' + question + '\n'
			data.write(tempStr)
			print(tempStr)
	i+=1


 