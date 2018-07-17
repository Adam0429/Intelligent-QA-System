import pickle
import pymysql
import re
from tqdm import tqdm
import jieba.posseg as pseg
import jieba

# jieba.load_userdict('dict.txt')


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


def tokenization(text):
    stop_flag = ['x', 'c', 'u', 'p', 't', 'uj', 'm', 'f', 'r']
    result = []
    words = pseg.cut(text)
    allwords = ' '.join(jieba.cut(text, cut_all=True)).split()
    for word, flag in words:
        if flag in stop_flag and word in allwords:
            allwords.remove(word)
    allwords = list(set(allwords))
    return ','.join(allwords)


# f = open("bm25.model", "rb")
# bin_data = f.read()
# data = pickle.loads(bin_data)
# for d in data['answers']:
#     print(d)


# from gensim.summarization.bm25 import get_bm25_weights
# corpus = [
#     ["black", "cat", "white", "cat"],
#     ["cat", "outer", "space"],
#     ["wag", "dog"]
# ]
# result = get_bm25_weights(corpus)
# print(result)

db = pymysql.connect("localhost", "root", "970429",
                     "test", charset="utf8mb4")
cursor = db.cursor()
cursor.execute('select normal_question from QA')
for c in tqdm(cursor.fetchall()):
    cursor.execute('update QA set descs_words="' +
                   tokenization(c[0]) + '" where normal_question="' + c[0] + '"')

cursor.execute('select answer from QA')
for c in tqdm(cursor.fetchall()):
    cursor.execute('update QA set answer_words="' +
                   tokenization(del_tag(c[0])) + '"' + " where answer='" + c[0] + "'")
db.commit()

# data = {}
# data['descs'] = []
# data['answers'] = []
# data['title'] = []

# db = pymysql.connect("localhost", "root", "970429",
#                      "test", charset="utf8mb4")
# cursor = db.cursor()
# cursor.execute('select answer from QA')
# for c in tqdm(cursor.fetchall()):
#     data['answers'].append(tokenization(del_tag(c[0])))
# cursor.execute('select normal_question from QA')
# for c in cursor.fetchall():
#     data['title'].append(c[0])
#     data['descs'].append(tokenization(c[0]))

# output = open('bm25.model', 'wb')
# pickle.dump(data, output)
