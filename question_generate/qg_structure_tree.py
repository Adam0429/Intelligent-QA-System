# -*- coding: utf-8 -*-
#作者：Zhang Qinyuan
#python 版本：3.6
#更新时间 2018/3/18
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
def generator(sentence):
    labels = splitor(sentence)
    useful_labels = filter(labels)
    #找到最后一个标签
    last_label = segmentor(useful_labels[-1])
    #记录最后一个标签的所有词性
    last_label_postages = posttagger(last_label)

    #假如最后一个标签的开头是“什么”，则不需要生成问题
    if (
        last_label[0] == '什么' or
        last_label[0] == '怎么' or
        last_label[0] == '如何'
    ):
        str = ''
        print(str.join(last_label))

    #假如最后一个标签的开头是动词，则用“怎么... ...”生成问句
    elif last_label_postages[0] is 'v':
        #假如最后一个标签只有一个动词，例如“入门”
        if len(last_label_postages) == 1:
            print('怎么' + last_label[0] + useful_labels[0] + '？')
        else:
            #假如只有一个动词加其他词，例如“管理集群”
            if (
                '和' not in last_label and
                '或' not in last_label
            ):
                str = ''
                print('怎么' + last_label.pop(0) + useful_labels[0] + '的' + str.join(last_label) + '？')
            #假如超过一个动词，例如“访问和使用DWS”
            else:
                last_label_postages.reverse()
                index_of_last_v = len(last_label_postages) - last_label_postages.index('v')
                last_label_postages.reverse()
                str = ''
                #假如只有动词
                if last_label_postages[-1] is 'v':
                    print('怎么' + str.join(last_label[:index_of_last_v]) + useful_labels[0] + '？')
                #假如有其他词
                else:
                    print('怎么' + str.join(last_label[:index_of_last_v]) + useful_labels[0] + '的' + str.join(last_label[index_of_last_v:]) + '？')

    #假如最后一个标签的开头是名词，则用“... ...有哪些”生成问句
    elif (
        last_label_postages[0] is 'n' or
        last_label_postages[0] is 'a' or
        last_label_postages[0] is 'b'
    ):
        str = ''
        print(useful_labels[0] + '的' + str.join(last_label) + '有哪些？')


print('******************整体测试：**********************')
generator('帮助中心 > 镜像服务 > 用户指南 > 管理 > 共享镜像 > 附录')

#print('******************分部份测试，将会顺序执行：**********************')
#labels = splitor()
#筛选
#useful_labels = filter(labels)
#print('###############以上为筛选结果###############')
#测试分词
#for label in useful_labels:
#    words = segmentor(label)
#    tags = posttagger(words)
#    print()
#print('###############以上为分词测试###############')

#难以处理的标签：
#"续费"：被标记名词
#"使用限制"：不同于其他动词开头
#"计费方式"：不同于其他动词开头
#"操作指南"：不同于其他动词开头
#"准备工作"：不同于其他动词开头

#词性表：
#http://ltp.readthedocs.io/zh_CN/latest/appendix.html#id3