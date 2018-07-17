from openpyxl import Workbook
import pymysql
from tqdm import tqdm

wb = Workbook()
sheet = wb.active
sheet.title = 'sheet 1'
db = pymysql.connect("localhost", "root", "970429", "test", charset="utf8mb4")
cursor = db.cursor()
cursor.execute('select normal_question,answer,url from QA')
index = 1
for c in tqdm(cursor.fetchall()):
    index += 1
    sheet['A' + str(index)] = c[0]
    sheet['B' + str(index)] = c[1]
    sheet['C' + str(index)] = c[2]


wb.save('1.xlsx')
