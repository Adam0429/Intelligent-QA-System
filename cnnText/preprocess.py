import os
import random

"""
将文本整合到 train、test、val 三个文件中
"""

count = 1
lineArray = []
f = open('question.txt', 'r', encoding='UTF-8')

tempStr = f.readline()
while tempStr:
	tempStr = tempStr.strip()
	tempList = tempStr.split(':')
	str1 = tempList[0]
	str2 = tempList[1]
	finalStr = str2 + '\t' + str1 + '\n'
	lineArray.append(finalStr)
	tempStr = f.readline()
	count += 1
f.close()

random.shuffle(lineArray)

output1 = open('cnews.train.txt', 'w', encoding='UTF-8')
output2 = open('cnews.test.txt', 'w', encoding='UTF-8')
output3 = open('cnews.val.txt', 'w', encoding='UTF-8')
for i in range(0,len(lineArray)):
	if i < 945:
		output1.write(lineArray[i])
	elif i < 1350:
		output2.write(lineArray[i])
	else:
		output3.write(lineArray[i])
output1.close()
output2.close()
output3.close()
print(count)