#!/usr/bin/python
# encoding: utf-8
"""
作者:糖葫芦
创建时间:2020/5/2316:02
文件:preprocess.py
IDE:PyCharm
"""
import numpy as np
import pandas as pd
import re
from jieba import posseg
import jieba
from K01_word2vec.tokenizer import segment
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REMOVE_WORDS = ['|', '[', ']', '语音', '图片', ' ']


def read_stopwords(path):
    lines = set()
    with open(path, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            lines.add(line)
    return lines


def remove_words(words_list):
    words_list = [word for word in words_list if word not in REMOVE_WORDS]
    return words_list


def parse_data(train_path, test_path):
    train_df = pd.read_csv(train_path, encoding='utf-8')
    # subset参数删除该字段中含有空值的全部行, how:不再使用向后兼容, inplace 是否在当前对象上执行删除操作
    train_df.dropna(subset=['Report'], how='any', inplace=True)
    train_df.fillna('', inplace=True)
    train_x = train_df.Question.str.cat(train_df.Dialogue)

    print('train_x is ', len(train_x))
    train_x = train_x.apply(preprocess_sentence)
    print('train_x is ', len(train_x))
    train_y = train_df.Report
    print('train_y is ', len(train_y))
    train_y = train_y.apply(preprocess_sentence)
    print('train_y is ', len(train_y))
    # if 'Report' in train_df.columns:
        # train_y = train_df.Report
        # print('train_y is ', len(train_y))

    test_df = pd.read_csv(test_path, encoding='utf-8')
    test_df.fillna('', inplace=True)
    test_x = test_df.Question.str.cat(test_df.Dialogue)
    test_x = test_x.apply(preprocess_sentence)
    print('test_x is ', len(test_x))
    test_y = []
    train_x.to_csv('F:\开课吧\自然语言处理\数据\\train_set.seg_x.txt', index=None, header=False)
    train_y.to_csv('F:\开课吧\自然语言处理\数据\\train_set.seg_y.txt', index=None, header=False)
    test_x.to_csv('F:\开课吧\自然语言处理\数据\\test_set.seg_x.txt', index=None, header=False)


def preprocess_sentence(sentence):
    seg_list = segment(sentence.strip(), cut_type='word')
    seg_list = remove_words(seg_list)
    seg_line = ' '.join(seg_list)
    return seg_line


if __name__ == '__main__':
    # 需要更换成自己数据的存储地址
    parse_data('F:\开课吧\自然语言处理\数据\AutoMaster_TrainSet.csv',
               'F:\开课吧\自然语言处理\数据\\test.csv')


