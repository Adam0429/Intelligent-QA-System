from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser
import codecs
from tqdm import tqdm
import time
import os
import re
from bs4 import BeautifulSoup
import pymysql

db = pymysql.connect("localhost", "root", "970429", "test", charset="utf8mb4")
cursor = db.cursor()
# idx = 1


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


path = '/home/wangfeihong/桌面/support.huaweicloud.com/'
files = os.listdir(path)
for file in tqdm(files):
    data = {}
    f = open(path + file, mode='r')
    text = f.read()
    if not 'developer' in file:
        soup = BeautifulSoup(text, 'lxml')
        elements = soup.select('.help-link')
        h1s = soup.select('h1')
        t = del_tag(elements)
        if "上一篇" in text:
            t.remove(t[len(t) - 1])
        if "下一篇" in text:
            t.remove(t[len(t) - 1])
        soup2 = BeautifulSoup(text, 'lxml')
        details = soup.select('.help-details')
        if len(details) == 0:
            details = soup.select('div[id^="body"]')
        if len(details) == 0:
            details = soup.select('.beg-text')
        if len(details) == 0:
            details = soup.select('.periods')
        if len(details) == 0:
            details = soup.select('.help-main')
        if len(details) == 0:
            details = soup.select('.helpContent')
        if len(details) == 0:
            details = soup.select('.record-content')
        if len(details) == 0:
            details = soup.select('.content-block')
        if len(details) == 0:
            # print('!!!!!:'+file)
            continue
        # 正常是所有页面都有一个div储存问答信息,类名不一定是什么，大概就上面几种
        details = str(details)
        soup = BeautifulSoup(details, 'lxml')
        soup2 = BeautifulSoup(text, 'lxml')
        descs = soup2.select('.crumbs')
        # soup3 = BeautifulSoup(str(descs),'lxml')
        desc = []

        if len(descs) == 0:
            descs = soup2.select('.position')
        if len(descs) != 0:
            for c in descs[0].children:
                if not c.isspace:
                    desc.append(del_tag(c))
            data['desc'] = desc
        if 'desc' not in data:
            data['desc'] = ['null']

        h1 = soup2.h1
        # print(data['desc'])
        h5s = soup.select('h5')
        h4s = soup.select('h4')
        h3s = soup.select('h3')
        h2s = soup.select('h2')
        h1s = soup.select('h1')
        hs = h1s + h2s + h3s + h4s + h5s
        questions = {}
        qas = {}
        for h in hs:
            index = details.find(str(h))
            questions[h] = index

        questions = sorted(questions.items(), key=lambda abs: abs[1])  # tuple
        # 还有种没标题的
        try:
            if len(hs) == 0:
                question = data['desc'][len(data['desc']) - 1]
                answer = details.split(str(descs[0]))
                # print(answer[len(answer)-1])
                qas[del_tag(question)] = answer[len(answer) - 1]
            if len(questions) == 1:
                answer = details.split(str(h))[1]
                answer = answer.replace('\n', '')
                answer = answer.replace("'", "''")
                if '父主题' in answer:
                    answer = answer.split('父主题')[0]
                qas[del_tag(questions[0][0])] = answer
            else:
                for i in range(len(questions) - 1):
                    # print(questions[i][0])
                    # print(questions[i+1][0])
                    content = details.split(str(questions[i][0]))[1]
                    content = content.split(str(questions[i + 1][0]))[0]
                    answer = content
                    if '父主题' in answer:
                        answer = answer.split('父主题')[0]
                    qas[del_tag(questions[i][0])] = answer
        except:
            print(file + '=============')
        data['url'] = file
        data['qas'] = qas

    # developer
    else:
        soup = BeautifulSoup(text, 'lxml')
        details = str(soup.select('#content'))
        soup = BeautifulSoup(str(details), 'lxml')
        descs = soup.select('.crumbs')
        titles = soup.select('span')
        h1 = soup.h1
        if len(descs) == 0:
            descs = soup.select('.position')
        if len(descs) != 0:
            for c in descs[0].children:
                if not c.isspace:
                    desc.append(del_tag(c))
            data['desc'] = desc
        else:
            data['desc'] = [del_tag(str(soup.h1))]
        # if h1 is None:
        h5s = soup.select('h5')
        h4s = soup.select('h4')
        h3s = soup.select('h3')
        h2s = soup.select('h2')
        h1s = soup.select('h1')
        hs = h1s + h2s + h3s + h4s + h5s
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 想法是找到每个h4的位置,每两个h4的之间的内容就是第一个h4的答案,原先找h4的子节点方法不可用，因为网页写得太乱,div有些包括答案和内容，有些不包括
        # 如果小标题都没有，直接拿h1做问题，剩下的都是答案
        qas = {}
        questions = {}
        for h in hs:
            index = details.find(str(h))
            questions[h] = index
        questions = sorted(questions.items(), key=lambda abs: abs[1])  # tuple
        # print(questions)
        try:
            if len(hs) == 0:
                question = data['desc'][len(data['desc']) - 1]
                answer = details.split(str(descs[0]))
                # print(answer[len(answer)-1])
                qas[del_tag(question)] = answer[len(answer) - 1]
            if len(questions) == 1:
                answer = details.split(str(h))[1]

                if '父主题' in answer:
                    answer = answer.split('父主题')[0]
                qas[del_tag(questions[0][0])] = answer
            else:
                for i in range(len(questions) - 1):
                    # print(questions[i][0])
                    # print(questions[i+1][0])
                    content = details.split(str(questions[i][0]))[1]
                    content = content.split(str(questions[i + 1][0]))[0]
                    answer = content
                    answer = answer.replace('\n', '')
                    answer = answer.replace("'", "''")
                    if '父主题' in answer:
                        answer = answer.split('父主题')[0]
                    qas[del_tag(questions[i][0])] = answer
        except:
            continue
            print('file' + '=====================')
        # ------------------------------
        data['url'] = file
        data['qas'] = qas

    # print(generator(_segmentor,_postagger,data['desc']))
    for question, answer in data['qas'].items():
        # idx = idx + 1
        dd = []
        for d in data['desc']:
            # if d != data['desc'][len(data['desc'])-1]:
            dd.append(d)

        # question = question.replace('\n','')
        # question = question.strip()
        dd.append(question)
        d = ' '.join(dd)
        question = '-'.join(dd)
        answer = answer.replace('\n', '')
        answer = answer.replace("'", '"')
        answer = answer.replace(';', '')
        answer = answer.replace('”', '"')
        answer = answer.replace('“', '"')
        # some limit signals in sql
        if del_tag(answer) == '':
            # print(answer)
            continue
        # answer is null
        sql = 'insert into QA values("' + question + '",' + '"null"' + ",'" + \
            data['url'] + "','" + answer + "','null'" + ",'null'" + ")"
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            e = str(e)
            e = e.split(',')[0][1:]
            if e == '1062':  # duplicate
                # print(file)
                sql = 'select answer,url from QA where normal_question="' + question + '"'
                cursor.execute(sql)
                db.commit()
                result = cursor.fetchall()[0]
                url = result[1] + ' ' + data['url']
                result = result[0]
                # print(url)
                if del_tag(result) != del_tag(answer):
                    answer = answer + result[0]
                    answer = answer.replace('\n', '')
                    answer = answer.replace("'", '"')
                    answer = answer.replace(';', '')
                    answer = answer.replace('”', '"')
                    answer = answer.replace('“', '"')
                    answer = answer + result
                    # ~~~~~~~~~~~
                sql = "update QA set answer='" + answer + \
                    "' where normal_question='" + question + "'"
                sql2 = "update QA set url='" + url + "' where normal_question='" + question + "'"
                # print(sql2)
                # have the same answer situation
                cursor.execute(sql)
                cursor.execute(sql2)
                # print(url)
                db.commit()
            elif e == '1064':  # limit signals
                # print(file)
                answer = del_tag(answer)
                sql = 'insert into QA values("' + question + '","' + '"null"' + ",'" + \
                    data['url'] + "','" + answer + \
                    "','null'" + ",'null'" + ")"
                cursor.execute(sql)
                db.commit()
