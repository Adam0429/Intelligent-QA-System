# -*- coding: utf-8 -*-
#作者：Zhang Qinyuan
#python 版本：3.6
#更新时间 2018/3/23
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser

#分隔标签
def splitor(sentence='帮助中心 > 数据仓库服务 > 购买指南 > 续费'):
    labels_list = list(sentence.split(' > '))
#   for label in labels_list:
#       print(label + ' ', end = '')
    return labels_list

def filter(List):
    useless_labels = ['简介','帮助中心','概览','产品简介','快速入门','FAQ','用户指南']
    nList = list()
    for label in List:
        if label not in useless_labels:
            nList.append(label)
#    for label in nList:
#        print(label + ' ', end = '')
#    print()
    return nList;

#分词
def segmentor(sentence=''):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/cws.model')  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

#获取分词后词性
def posttagger(words):
    postagger = Postagger() # 初始化实例
    postagger.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/pos.model')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
#   for word,tag in zip(words,postags):
#       print (word+'/'+tag)
    postags_list = list(postags)
    postagger.release()  # 释放模型
    return postags_list

#生成问句
def generator(List,qas):
    labels = List
    useful_labels = filter(labels)
    # 找到最后一个标签
    last_label = segmentor(useful_labels[-1])
    # 记录最后一个标签的所有词性
    last_label_postages = posttagger(last_label)
    # 小标题分词
    qas_list = segmentor(qas)
    # 记录小标题的所有词性
    qas_postages = posttagger(qas_list)

    #假如小标题是概述或者描述整个页面的，则忽略该问题
    if qas == '概述':
        return

    #假如小标题的开头是动词，且分词后大于3个词汇，用"怎么... ..."来生成
    elif (qas_postages[0] is 'v' and
        len(qas_list) > 2):
        return '怎么' + qas

    #假如小标题的开头是操作，则用"...的...有哪些"来生成
    elif (qas_list[0] == '操作' or
          qas_list[0] == '使用'):
        return useful_labels[-1] + '的' + qas + '有哪些？'

    #假如小标题分词后第一个词为名词，则用"有哪些... ..."来生成
    elif (
        qas_postages[0] == 'n' or
        qas_postages[0] == 'nt' or
        qas_postages[0] == 'nz'
    ):
        return '有哪些' + qas

print('******************整体测试：**********************')
a = generator(splitor('帮助中心 > 弹性云服务器 > 用户指南 > 实例 > 用户数据注入'),'使用场景')
print(a)