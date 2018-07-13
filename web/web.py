from flask import Flask, abort, request, redirect, render_template, jsonify
import copy
from flask_script import Manager
# from flask_bootstrap import Bootstrap
# from wtforms import StringField,SubmitField
# from wtforms.validators import Required
import jieba.posseg as pseg
import codecs
import pymysql
from tqdm import tqdm
from gensim import corpora
import bm25
from bm25 import get_bm25_weights
import os
import re
import pickle
import jieba
from jieba import analyse
import pymysql

app = Flask('my web')
app.config['SECRET_KEY'] = '1234231'


def load_similardict(path):
    print('loading similar model...')
    similar_dict = {}
    for line in open(path, 'rU', encoding='utf-8'):
        words = line.strip().split('-')
        for w in words:
            similar_dict[w] = words
    return similar_dict


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


def del_div(strings):
    dr = re.compile(r'<div[^>]+>', re.S)
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


def find_a(strings):
    regex = re.compile('<a.*>')
    string = regex.findall(strings)
    if len(string) != 0:
        return string[0]
    else:
        return ''


# def f1(result):
#     best_answer = [result[0]]
#     min_word = len(result[0][0].split('-'))
#     # print(result)
#     for r in result:
#         length = len(r[0].split('-'))
#         # print(r)
#         # print(length)
#         # 先取出字条数最少的，再在其中找到长度最短的
#         # 改成计算文本相似度
#         if length < min_word:
#             min_word = length
#             best_answer = [r]
#         if length == min_word:
#             best_answer.append(r)
#     best = best_answer[0]
#     num = len(best_answer[0])
#     for b in best_answer:
#         length = len(b[0])
#         if length < num:
#             best = b
#     return best


def andsearch(keywords, attr, attr2):
    first = True
    sql = 'select ' + attr + ' from QA where '
    for w in keywords:
        if first:
            sql = sql + attr2 + ' like "%' + w + '%" '
            first = False
        else:
            sql = sql + 'and ' + attr2 + ' like "%' + w + '%" '
    return sql


def orsearch(keywords, attr, attr2):
    first = True
    sql = 'select ' + attr + ' from QA where '
    for w in keywords:
        if first:
            sql = sql + attr2 + ' like "%' + w + '%" '
            first = False
        else:
            sql = sql + 'or ' + attr2 + ' like "%' + w + '%" '
    return sql


def tokenization(text):
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']
    result = []
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag:
            result.append(word)
    return result


def get_keywords(query):
    keywords = analyse.extract_tags(query, withWeight=False)
    # allowPOS=['ns','n','vn','v','nr']
    # 处理大小写不能分出关键词的问题,分词区分大小写,而数据库查询不区分
    # keywords = ['帮助中心','产品术语-驱动']
    # 如没有关键词,就需要分词将所有词做关键词
    if len(keywords) == 0:
        keywords = jieba.cut(query, cut_all=True)
        keywords = '/'.join(keywords)
        keywords.split('/')
    return keywords


def get_questionword(query):
    questionword = ''
    for qw in questionwords:
        if qw in query:
            return qw
    return None


def bm25_score(corpus, keywords):
    bm25Model = bm25.BM25(corpus)
    average_idf = sum(map(lambda k: float(
        bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(keywords, average_idf)
    return scores


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    args = request.args.to_dict()
    title = args['question']
    keywords = args['keywords']
    keywords = keywords.split(' ')

    # print(keywords)
    db = pymysql.connect("localhost", "root", "970429",
                         "test", charset="utf8mb4")
    cursor = db.cursor()
    print('select descs from QA where normal_question = "' + title + '"')
    cursor.execute(
        'select descs from QA where normal_question = "' + title + '"')

    result = cursor.fetchall()[0][0]
    new_result = str(result)
    for keyword in keywords:
        if keyword not in result:
            new_result += ' ' + keyword
            print('add ' + keyword + ' to ' + title)
    if new_result != result:
        print("update QA set descs='" + new_result +
              "' where normal_question='" + title + "'")
        cursor.execute("update QA set descs='" + new_result +
                       "' where normal_question='" + title + "'")
        db.commit()
        cursor = db.cursor()
        data = {}
        data['descs'] = []
        data['answers'] = []
        cursor.execute('select answer from QA')
        for c in tqdm(cursor.fetchall()):
            data['answers'].append(del_tag(c[0]))
        cursor.execute('select descs from QA')
        for c in cursor.fetchall():
            data['descs'].append(c[0])
        output = open('bm25.model', 'wb')
        pickle.dump(data, output)
        return 'update'
    return 'did not update'


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')


@app.route('/getanswer', methods=['GET', 'POST'])
def getanswer():
    db = pymysql.connect("localhost", "root", "970429",
                         "test", charset="utf8mb4")
    cursor = db.cursor()
    query = request.args['question']
    keywords = tokenization(query)
    # keywords = get_keywords(query)
    ky = keywords
    # origin keywords
    print(keywords)
    keys = '-'.join(keywords)
    questionword = get_questionword(query)

    descs = []
    corpus = []

    f = open("bm25.model", "rb")
    bin_data = f.read()
    data = pickle.loads(bin_data)
    answers = data['answers']
    descs = data['descs']
    origins = data['title']

    print('keywords')
    if '服务' in keywords and len(keywords) > 1:
        keywords.remove('服务')
    print(keywords)

    descs_score = bm25_score(descs, keywords)
    answers_score = bm25_score(answers, keywords)
    total_score = []
    for i in range(0, len(answers)):
        total_score.append(descs_score[i] * 10 + answers_score[i])
    _scores = list(set(total_score))
    _scores.sort(reverse=True)

    answer = ''
    url = []
    titles = []
    # for s in _scores[:13]:
    #     print(s)
    #     idx = scores.index(s)
    #     print(scores[idx])
    # idx = scores.index(s)
    # cursor.execute('select url from QA where descs = "' + descs[idx] + '"')
    # url.append(cursor.fetchall()[0][0])

    url = list(set(url))

    # if len(url) == 1:
    #     # print(url)
    #     # cursor.execute('select descs from QA where url = "'+url[0]+'"')
    #     # for c in cursor.fetchall():
    #     #   titles.append(c[0])
    #     for s in _scores[:3]:
    #         idx = total_score.index(s)
    #         titles.append(origins[idx])
    #         print(descs[idx])
    #         print(total_score[idx])

    # else:
    for s in _scores[:3]:
        idx = total_score.index(s)
        titles.append(origins[idx])
        print(descs[idx])
        print(total_score[idx])

    totalanswer = ''
    for title in tqdm(titles):
        # print(title)
        sql = 'select normal_question,answer from QA where descs="' + title + '"'
        cursor.execute(sql)
        result = cursor.fetchall()
        title = result[0][0]
        answer = '<h2>' + title + '</h2><d>' + result[0][1]
        # print(cursor.fetchone())
        if del_tag(answer) == title:
            answer = '<h2>' + title + '</h2><d>' + find_a(answer) + '链接'
        totalanswer = totalanswer + answer + \
            '<key style="color:#fff">' + keys + '</key>' + '<split>'

    totalanswer = del_div(totalanswer)
    totalanswer = totalanswer.replace('</div>', '')
    totalanswer = totalanswer.replace(']', '')
    #totalanswer = '<div>' + totalanswer + '</div>'
    # print(totalanswer)
    return totalanswer
    # 取前3个排序,如来自同一网页则返回网页下所有内容,不是则都返回


if __name__ == '__main__':
    # jieba.load_userdict('dict.txt')
    similar_dict = load_similardict('jinyici.txt')
    questionwords = similar_dict.keys()
    questionwords = list(questionwords)
#   questionwords.remove('')
    app.run(host='0.0.0.0', port=5000, debug=True)
