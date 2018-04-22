import jieba.posseg as pseg
import codecs
import pymysql
from tqdm import tqdm
from gensim import corpora
from gensim.summarization import bm25
from gensim.summarization.bm25 import get_bm25_weights
import os
import re
import pickle
import jieba
from jieba import analyse

jieba.load_userdict('dict.txt') 

def del_tag(strings):
    dr = re.compile(r'<[^>]+>',re.S)
    if type(strings) == type([]): 
        strs = []
        for string in strings:
            string = str(string)
            s = dr.sub('',string)
            strs.append(s)
        return strs
    else:
        strings= str(strings)
        s = dr.sub('',strings)
        return s

def f1(result):
    best_answer = [result[0]]
    min_word = len(result[0][0].split('-'))
    # print(result)
    for r in result:
        length = len(r[0].split('-'))
        # print(r)
        # print(length)
        # 先取出字条数最少的，再在其中找到长度最短的
        # 改成计算文本相似度
        if length < min_word:
            min_word = length
            best_answer = [r]
        if length == min_word:
            best_answer.append(r)
    best = best_answer[0]
    num = len(best_answer[0])
    for b in best_answer:
        length = len(b[0])
        if length < num:
            best = b
    return best 

def andsearch(keywords,attr):
    first = True
    sql = 'select ' + attr + ' from QA where '
    for w in keywords:
        if first:   
            sql = sql + 'descs like "%' + w + '%" '
            first = False
        else:
            sql = sql + 'and descs like "%' + w + '%" '
    return sql

def orsearch(keywords,attr):
    first = True
    sql = 'select ' + attr + ' from QA where '
    for w in keywords:
        if first:   
            sql = sql + 'descs like "%' + w + '%" '
            first = False
        else:
            sql = sql + 'or descs like "%' + w + '%" '
    return sql

def tokenization(text):
    result = []
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag:
            result.append(word)
    return result


query = input('')
keywords = analyse.extract_tags(query,topK=20, withWeight=False,allowPOS=['ns','n','vn','v','nr'])
# print(keywords)
# keywords = ['DevOps','解决方案']

sql = andsearch(keywords,'answer')
sql2 = orsearch(keywords,'answer')
db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
cursor = db.cursor()
cursor.execute(sql)
result = cursor.fetchall()
cursor.execute(sql2)
result2 = cursor.fetchall()
if len(result) == 0:
    if result2 == 0:
        result == None
    else:
        result = result2

corpus = []
stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
if result != None:
    for r in tqdm(result):
        text = del_tag(r)
        terms = tokenization(text)
        corpus.append(terms)
else:
    output = open('bm25.model', 'wb')
    pickle.dump(corpus,output)
    f = open("bm25.model","rb")
    bin_data = f.read()
    corpus = pickle.loads(bin_data)

bm25Model = bm25.BM25(corpus)
average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())


scores = bm25Model.get_scores(keywords,average_idf)
# scores.sort(reverse=True)
idx = scores.index(max(scores))
print(scores)
print(corpus[idx])
