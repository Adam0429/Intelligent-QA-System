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

# db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
# cursor = db.cursor()
# cursor.execute('select answer from QA')
# result = cursor.fetchall()

def tokenization(text):
    result = []
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag:
            result.append(word)
    return result

# corpus = []
# stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
# for r in tqdm(result):
#     text = del_tag(r)
#     terms = tokenization(text)
#     corpus.append(terms)
# output = open('data.pkl', 'wb')
# pickle.dump(corpus,output)

f = open("data.pkl","rb")
bin_data = f.read()
corpus = pickle.loads(bin_data)
bm25Model = bm25.BM25(corpus)
average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())


query = ['政策','服务器','法规']
scores = bm25Model.get_scores(query,average_idf)
# scores.sort(reverse=True)
idx = scores.index(max(scores))
print(idx)
print(corpus[idx])
