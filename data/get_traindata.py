import pymysql
import random

dictfile = open('traindata2.txt','r+')
db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
cursor.execute('select normal_question from QA ')
# where normal_question' like "%什么%" or normal_question like "%?%"')
result = cursor.fetchall()
result = list(result)
random.shuffle(result)
print(result)
text = ''
for r in result:
	# idx = len(r[0].split('-'))
	# text = text + (r[0].split('-'))[idx-1] + '\n'
	text = text + r[0] + '\n'
dictfile.write(text)
