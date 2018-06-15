import pymysql

db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
cursor.execute('select normal_question from QA')
results = cursor.fetchall()
for result in results:
	print(result[0])
	# ni fang fa xie zhe
	# result[0]  --->  type

	cursor.execute('update QA set type = ' + type + 'where normal_question == '+result[0])