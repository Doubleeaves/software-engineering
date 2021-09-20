# -*-coding:utf-8-*-
import sys
import time
import re
from typing import Any
import psutil
import os
# 一个装有给定关键字的常量列表
KEY_WORD = [
    "auto", "double", "int", "struct", "break", "else", "long", "switch",
    "case", "enum", "register", "typedef", "char", "extern", "return", "union",
    "const", "float", "short", "unsigned", "continue", "for", "signed", "void",
    "default", "goto", "sizeof", "volatile", "do", "if", "while", "static"
]
# 装有常用字符的常量列表
BRACKETS = [
    '(', ')', '{', '}', '<', '>', ',', ':', ';', '-', '+', '*', '/', '=', '^',
    '&', '|', '!', '%'
]


# 手动封装一个栈，让操作更加方便
class Stack():
    def __init__(self) -> None:
        self.__buffer = []

    def pop(self) -> Any:
        self.__buffer.pop()

    def push(self, elemt) -> Any:
        self.__buffer.append(elemt)

    def __len__(self):
        return len(self.__buffer)

    def top(self) -> Any:
        return self.__buffer[len(self.__buffer) - 1]


def readFile(filePath: str) -> list[str]:  # 读取文件内容
    lines = ""
    with open(filePath, encoding='utf-8') as file:  # 逐行读取
        for line in file:
            lines = lines + line
    lines = re.sub(r'\".*\"', '', lines)  # 正则匹配，将所有字符串删除
    lines = re.sub(r"//.*", '', lines)  # 正则匹配，将所有以 // 注释的内容删除
    lines = lines.replace('\n', '')  # 删除所有换行符
    lines = re.sub(r'/\*.*?\*/', '',
                   lines)  # 正则删除所有以 /**/注释的内容删除，采用非贪婪匹配，防止删除过多
    for i in BRACKETS:
        lines = lines.replace(i, ' ' + i + ' ')  # 将所有非字母或数字的字符前后各插入一个空格，方便操作
    lines = lines.split(' ')  # 以空格为界切割所有单词
    while True:  # 删除所有的空字符
        try:
            lines.remove('')
        except Exception:
            break
    return lines


# 查找if - else和if-elif-else结构的数量，采用花括号匹配逆序遍历
# data为传入需要查找的字符串列表，ifDic为计数两种if-else情况的字典
# status为True时，函数处于递归态，rightBrackets为存储'}'的栈
# 结果通过ifDic来展示
def searchIfElse(
    data: list[str],
    ifDic: dict,
    status=False,
    rightBrackets=Stack()
) -> int:
    index = len(data) - 1  # 从尾端开始遍历
    flag = False  # 设置标志，True为遇到else，False为未遇到else
    ifType = 0  # 1为if-elif-else格式 0为if-else格式
    stackCount = 0  # 记录遇到else时的堆栈长度，遇到if时判断是否与else匹配
    while index >= 0:
        if data[index] == 'else':
            if flag is False:
                flag = True
                stackCount = len(rightBrackets)
            else:
                index = searchIfElse(data[:index + 1], ifDic, True,
                                     rightBrackets)  # 若else前又遇到else，则递归处理
        elif data[index] == 'if':
            if flag is True and len(
                    rightBrackets
            ) == stackCount:  # stackCount与当前栈长相同，则匹配成功，相应的类型+1，否则失败
                ifDic[ifType] += 1
                flag = False  # 成功时将标志重置
                if status is True:  # 若是处于递归，则退出
                    return index
            ifType = 0
        elif data[index] == 'elif' and flag is True:
            ifType = 1
        elif data[index] == '{':
            rightBrackets.pop()
        elif data[index] == '}':
            rightBrackets.push('{')
        index -= 1
    return 0


# 查找switch-case的数量，正序括号匹配遍历,data为传入的匹配列表，caseNum为统计case的列表
# status为True时函数处于递归态，switchTimes为统计switch出现的次数，函数结果由caseNum列表体现
def searchSwitch(data: list[str],
                 caseNum: list,
                 switcTimes: int = 0,
                 status=False) -> int:
    index = 0
    stack = Stack()
    num = 0
    flag = False  # 标志位，判断是否遇到switch False 为未遇到switch或已经匹配，True为遇到switch
    while index < len(data):
        if data[index] == 'switch':
            if flag is False:
                flag = True
                switcTimes += 1  # 记录碰到switch的次数
            else:  # 出现套娃，递归处理
                index = searchSwitch(data[index:], caseNum, switcTimes,
                                     True) + index
        elif data[index] == 'case' and flag is True:
            num += 1
        elif data[index] == '{' and flag is True:
            stack.push('{')
        elif data[index] == '}' and flag is True:
            stack.pop()
            if len(stack) == 0:  # 为空栈，则一个switch内容结束，记录数值
                caseNum.append(str(switcTimes) + ' ' + str(num))
                num = 0
                flag = False
                switcTimes += 1
                if status is True:  # status为True，则为递归，到此退出递归
                    return index
                else:
                    switcTimes += 1
        index += 1
    caseNum.sort()
    index = 0
    while index < len(caseNum):
        caseNum[index] = caseNum[index][2:]
        index += 1
    return index


def searchKeyWords(data: list[str]) -> int:  # 暴力遍历所有单词
    index = -1
    keyDic = {}
    for i in KEY_WORD:
        keyDic[i] = 0
    while index < len(data):
        index += 1
        try:
            keyDic[data[index]] += 1
            if data[index] == 'if':
                if data[index - 1] == 'else':  # 对 else if 结构进行处理，为接下来的要求做准备
                    data[index] = 'elif'
                    data.pop(index - 1)
                    index -= 1
        except Exception:
            continue
    num = 0
    for value in keyDic.values():
        num += value
    return num


if __name__ == '__main__':
    path = "C://vscode//.vscode//plane.cpp"
    level = 4
    if len(sys.argv) == 3:
        path = sys.argv[1]
        level = int(sys.argv[2])
    start = time.time()
    string = readFile(path)
    if level >= 1:
        num = searchKeyWords(string)
        print('total num: ' + str(num))
    if level >= 2:
        caseNum = []
        searchSwitch(string, caseNum)
        print('switch num: ' + str(len(caseNum)))
        print('case num: ', end='')
        for i in caseNum:
            print(i, end=' ')
        print()
    if level > 2:
        ifDic = {0: 0, 1: 0}
        searchIfElse(string, ifDic)
        if level >= 3:
            print('if-else num: ' + str(ifDic[0]))
        if level >= 4:
            print('if-elseif-else num: ' + str(ifDic[1]))
    print('total time is: ' + str(time.time() - start) + 'ms')
    print('using %.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
