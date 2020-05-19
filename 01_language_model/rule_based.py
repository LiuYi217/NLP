#!/usr/bin/python
# encoding: utf-8
"""
作者:糖葫芦
创建时间:2020/5/1820:04
文件:rule_based.py
    该文件用于学习和实践基于规则生成句子
IDE:PyCharm
"""
import random


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


def create_grammar(grammar_str, split, line_split):
    grammar = {}
    for line in grammar_str.split(line_split):
        if line == "":
            continue
        # action = line.split(split)
        # rule = [i.split() for i in action[1].split("|")]
        # grammar[action[0].strip()] = rule
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [i.split() for i in stmt.split("|")]
    return grammar


def generate(gram, target):
    choice = random.choice
    if target not in gram:
        return target
    tar = gram[target]
    sentences = [generate(gram, i) for i in choice(tar)]
    return ''.join([e for e in sentences])
    # [[['早上好'], ['服宝']], ['怎么样'], [['反记账']]]


def generate_n(num, gram, target):
    sentences = []
    for i in range(num):
        sentences.append(generate(gram, target))
    return "\n".join(sentences)


if __name__ == '__main__':
    human = create_grammar(human, "=", "\n")
    robot = create_grammar(robot, "=", "\n")
    humans = generate_n(20, human, 'human')
    robots = generate_n(20, robot, 'robot')
    print(humans)
    print(robots)
