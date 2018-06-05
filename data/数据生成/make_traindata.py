import random
words = open('words.txt','r')
model = open('model.txt','r')
data = open('data.txt','r+')
words_lines = words.readlines()
data_lines = model.readlines()
newlines = []
for line in words_lines:
	newlines.append(line[:2])
for line in data_lines:
	question = line.strip()
	words = random.sample(newlines,10)
	for word in words:
		print(question.replace('*',word))

