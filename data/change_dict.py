words = set()
file_object = open('descs.txt','r', encoding="utf-8")
postingDict = dict()
key = 0
for line in file_object:
    nLine = line.strip().replace("['","").replace("']","")
    nList = list(nLine.split("', '"))
    postingDict[key] = nList
    key += 1

for key,value in postingDict.items():
	for v in value:
		words.add(v + ' 3 ' + 'n')
with open('dict.txt','r+') as f:
	for word in words:
		f.write(word)
		f.write('\n')
