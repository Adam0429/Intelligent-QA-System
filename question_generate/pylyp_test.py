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

#分词
def segmentor(sentence='机器学习服务可降低机器学习使用门槛，提供可视化的操作界面来编排机器学习模型的训练、评估和预测过程，无缝衔接数据分析和预测应用，降低机器学习模型的生命周期管理难度，为用户的数据挖掘分析业务提供易用、高效、高性能的平台服务。'):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/cws.model')  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    print ('\t'.join(words))
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

def posttagger(words):
    postagger = Postagger() # 初始化实例
    postagger.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/pos.model')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word,tag in zip(words,postags):
        print (word+'/'+tag)
    postagger.release()  # 释放模型
    return postags

#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='机器学习(Machine Learning, ML)是一门多领域交叉学科，涉及概率论、统计学、逼近论、凸分析、算法复杂度理论等多门学科。专门研究计算机怎样模拟或实现人类的学习行为，以获取新的知识或技能，重新组织已有的知识结构使之不断改善自身的性能。'):
    sents = SentenceSplitter.split(sentence)  # 分句
    print ('\n'.join(sents))


#命名实体识别
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/ner.model')  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    i = 0
    for word, ntag in zip(words, netags):
        i = i + 1
        print (str(i) + '/' + word + '/' + ntag)
    recognizer.release()  # 释放模型
    return netags

#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    parser.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/parser.model')  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    #print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    i = 0
    for word, arc in zip(words, arcs):
        i = i + 1
        print (str(i) + '/' + str(arc.head) + '/' + str(arc.relation))
    parser.release()  # 释放模型
    return arcs

#角色标注
def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    labeller.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/srl')  # 加载模型
    roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    for role in roles:
        print (role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    labeller.release()  # 释放模型
#测试分句子
print('******************测试将会顺序执行：**********************')
#sentence_splitter('用户提交数据快递服务申请后，系统会生成磁盘签名文件，磁盘签名文件是服务单中磁盘的唯一标识，需要将其存放入磁盘根目录且不对其加密，然后将磁盘寄送到华为数据中心。华为数据中心管理员收到磁盘后直接将磁盘挂载到物理服务器上，系统会自动判断用户申请单中的信息与磁盘信息是否准确对应，磁盘信息匹配成功后，用户需填写AK/SK和加密密钥触发数据开始自动上传，数据上传过程中均无任何人工干预，以此来避免人为误操作。')
#print('###############以上为分句子测试###############')
#测试分词
words = segmentor('命名空间管理')
print('###############以上为分词测试###############')
#测试标注
tags = posttagger(words)
print('###############以上为词性标注测试###############')
#命名实体识别
netags = ner(words,tags)
print('###############以上为命名实体识别测试###############')
#依存句法识别
arcs = parse(words,tags)
print('###############以上为依存句法测试###############')
#角色标注
#roles = role_label(words,tags,netags,arcs)
#print('###############以上为角色标注测试###############')