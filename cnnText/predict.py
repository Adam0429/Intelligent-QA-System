# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr

from cnn_model import TCNNConfig, TextCNN
from data.cnews_loader import read_category, read_vocab

f = open('traindata.txt', 'r', encoding='UTF-8')
questionArray = []
tempStr = f.readline()
while tempStr:
    tempStr = tempStr.strip()
    questionArray.append(tempStr)
    tempStr = f.readline()
f.close()

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = 'data/cnews'
vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    cnn_model = CnnModel()
    words = open('traindata2.txt','r',encoding='UTF-8')
    output = open('biaozhu.txt', 'w', encoding='UTF-8')
    words_lines = words.readlines()
    for line in words_lines:
        templist = line.strip().split('-')
        tempStr = templist[len(templist)-2] + ' ' + templist[len(templist)-1]
        if len(templist) > 2:
            tempStr = templist[len(templist)-3] + ' ' + templist[len(templist)-2] + ' ' + templist[len(templist)-1]
        output.write(cnn_model.predict(tempStr) + '\t' + tempStr + '\n')
    output.close()
    # test_demo = ['云服务器好在哪',
    #              '弹性伸缩云是什么原因？',
    #             '功能介绍']
    # for i in test_demo:
    #     print(cnn_model.predict(i))
    # test_demo = questionArray
    # output = open('biaozhu.txt', 'w', encoding='UTF-8')

    # for i in test_demo:
    #     output.write(cnn_model.predict(i) + '\t' + i + '\n')
    #     print(cnn_model.predict(i))
    # output.close()
