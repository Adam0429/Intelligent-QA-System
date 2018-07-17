import jieba
import pymysql
from tqdm import tqdm
import re


def del_tag(strings):
    dr = re.compile(r'<[^>]+>', re.S)
    if type(strings) == type([]):
        strs = []
        for string in strings:
            string = str(string)
            s = dr.sub('', string)
            strs.append(s)
        return strs
    else:
        strings = str(strings)
        s = dr.sub('', strings)
        return s


fileSegWordDonePath = 'corpusSegDone.txt'
# read the file by line
fileTrainRead = []
#fileTestRead = []

db = pymysql.connect("localhost", "root", "970429",
                     "test", charset="utf8mb4")
cursor = db.cursor()
cursor.execute('select answer from QA')
for c in tqdm(cursor.fetchall()):
    fileTrainRead.append(del_tag(c[0]))

# define this function to print a list with Chinese


def PrintListChinese(list):
    for i in range(len(list)):
        print(list[i])


# segment word with jieba
fileTrainSeg = []
for i in range(len(fileTrainRead)):
    fileTrainSeg.append(
        [' '.join(list(jieba.cut(fileTrainRead[i][9:-11], cut_all=False)))])
    if i % 100 == 0:
        print(i)

# to test the segment result
# PrintListChinese(fileTrainSeg[10])

# save the result
with open(fileSegWordDonePath, 'wb') as fW:
    for i in range(len(fileTrainSeg)):
        fW.write(fileTrainSeg[i][0].encode('utf-8'))
        fW.write(b'\n')
