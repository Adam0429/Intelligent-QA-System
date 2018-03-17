
# -*- coding: utf-8 -*-
#作者：Zhang Qinyuan
#python 版本：3.6
#建立时间 2018/3/17
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser

#分隔标签
def splitor(sentence='帮助中心 > 数据仓库服务 > 用户指南 > 简介 > 数据仓库服务简介'):
    labels_list = list(sentence.split(' > '))
#   for label in labels_list:
#       print(label + ' ', end = '')
    return labels_list

#筛选有用数据
def filter(List):
    useless_labels = ['简介','帮助中心','概览','产品简介','价格说明','快速入门','FAQ','用户指南','概述','购买指南']
    nList = list()
    for label in List:
        if label not in useless_labels:
            nList.append(label)
    for label in nList:
        print(label + ' ', end = '')
    print()
    return nList;

#分词
def segmentor(sentence='镜像'):
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
    for word,tag in zip(words,postags):
        print (word+'/'+tag)
    postagger.release()  # 释放模型
    return postags

print('******************测试将会顺序执行：**********************')
labels = splitor()
#筛选
useful_labels = filter(labels)
print('###############以上为筛选结果###############')
#测试分词
for label in useful_labels:
    words = segmentor(label)
    tags = posttagger(words)
    print()
print('###############以上为分词测试###############')
#测试标注
#tags = posttagger(words)
#print('###############以上为词性标注测试###############')
#命名实体识别
#netags = ner(words,tags)
#print('###############以上为命名实体识别测试###############')
#依存句法识别
#arcs = parse(words,tags)
#print('###############以上为依存句法测试###############')
#角色标注
#roles = role_label(words,tags,netags,arcs)
#print('###############以上为角色标注测试###############')