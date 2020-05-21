#!/usr/bin/python
# encoding: utf-8
"""
作者:糖葫芦
创建时间:2020/5/2119:38
文件:2-gram.py
2-gram语言模型训练
IDE:PyCharm
"""
import pandas as pd
import jieba
import re
from collections import Counter
from L01_language_model import rule_based


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)
pd.set_option('display.width', 5000)
df = pd.read_csv("../data/movie_comments.csv", encoding='utf-8')
articles = df['comment'].dropna().tolist()
pattern = re.compile('\w+')


def token(string):
    return pattern.findall(string)
# for i in articles:
#     print(i)
#     print(pattern.findall(i))


articles_clean = ["".join(pattern.findall(i)) for i in articles]
with open('../data/article.txt', 'w', encoding='utf-8') as f:
    for a in articles_clean:
        f.write(a + '\n')

cut = jieba.cut
TOKEN = []
for i, line in enumerate(open('../data/article.txt', encoding='utf-8')):
    if i % 100 == 0:
        print(i)
    # if i > 1000:
    #     break
    TOKEN += cut(line)

words_count = Counter(TOKEN)


def tf(word):
    """
    计算词频：单词出现次数/所有单词出现次数
    :return:
    """
    return words_count[word]/len(TOKEN)


TOKEN_2_GRAM = [''.join(TOKEN[i:i+2]) for i in range(len(TOKEN[:-2]))]
words_count_2 = Counter(TOKEN_2_GRAM)


def tf_2(word1, word2):
    """
    2-gram词频统计加拉普拉斯平滑
    :param word1:
    :param word2:
    :return:
    """
    if word1+word2 in words_count_2:
        return words_count_2[word1+word2]/len(TOKEN_2_GRAM)
    else:
        return 1/len(TOKEN_2_GRAM)


def get_probality(sentence):
    """
    计算句子出现的可能性
    :param sentence:
    :return:
    """
    words = list(cut(sentence))
    pro = 1
    for i, word in enumerate(words[:-1]):
        next_word = words[i+1]
        probility = tf_2(word, next_word)
        pro *= probility
    return pro


if __name__ == '__main__':
    robot = '''
        robot = 称谓 我 回答
        称谓 = 人称 打招呼
        人称 = 你|您
        打招呼 = 好|早上好
        我 = 自报家门
        自报家门 = 我是服宝|我是机器人|我是你的小助手
        回答 = 肯定|否定|疑问
        肯定 = 这事我可以帮你|我能做这件事|没问题
        否定 = 抱歉我不能帮助你|我无法理解你的意思
        疑问 = 你是什么意思？|你在说什么？
    '''

    human = '''
        human = 寒暄 疑问 业务问题
        寒暄 = 打招呼 称呼|打招呼
        称呼 = 服宝|机器人
        打招呼 = 你好|早上好|中午好
        疑问 = 如何|怎么|怎么样
        业务问题 = 财税|名词
        财税 = 反记账|填制凭证
        名词 = 税务|报销
    '''
    human = rule_based.create_grammar(human, "=", "\n")
    robot = rule_based.create_grammar(robot, "=", "\n")
    humans = rule_based.generate_n(20, human, 'human')
    robots = rule_based.generate_n(20, robot, 'robot')
    res = sorted([(get_probality(i), i) for i in humans.split('\n')], key=lambda x: x[0])
    print(res)
