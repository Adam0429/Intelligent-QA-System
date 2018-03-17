# -*- coding: utf-8 -*-
#作者：Zhang Qinyuan
#python 版本：3.6
#更新时间 2018/3/18
import jieba.posseg as pseg

#def title_changing(sentence):
#	words = pseg.cut(sentence)
#	for word, flag in words:
#		if(flag == 'r'):
#			print(sentence+'？')
#			break


def single_def_line_changing(sentence):
	words = pseg.cut(sentence)
	for word, flag in words:
		if word == '是':
			print('是什么？')
			break
		elif word == '：' or word == ':':
			print('是什么？')
			break
		print(word, end = '')

def single_guide_line_changing(sentence):
	words = pseg.cut(sentence)
#	i = 0
#	v = 0
	word_list = []
	for word, flag in words:
#		i = i + 1
		if flag == 'v' or flag == 'vn' or flag == 'vd':
			word_list = []
		word_list.append(word)

	print('怎么', end = '')
	for x in word_list:
		print(x, end = '')

def single_info_line_changing(sentence):
	words = pseg.cut(sentence)
	word_list = []
	for word, flag in words:
		if flag == 'v':
			print(word + '什么？')
			break
		print(word, end = '')

single_info_line_changing("阿里云也提供了API接口方便您管理云服务器ECS")
