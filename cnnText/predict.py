# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr

from cnn_model import TCNNConfig, TextCNN
from data.cnews_loader import read_category, read_vocab

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
    # 人工测试在此输入
    test_demo = ['云服务器多少钱',
                 '张钦源是谁',
                 '智能问答系统是什么']
    for i in test_demo:
        print(cnn_model.predict(i))
