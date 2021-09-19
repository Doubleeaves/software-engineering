# -*-coding:utf-8-*-
# import sys
import time
import re
from typing import Any
KEY_WORD = [
    "auto", "double", "int", "struct", "break", "else", "long", "switch",
    "case", "enum", "register", "typedef", "char", "extern", "return", "union",
    "const", "float", "short", "unsigned", "continue", "for", "signed", "void",
    "default", "goto", "sizeof", "volatile", "do", "if", "while", "static"
]

BRACKETS = [
    '(', ')', '{', '}', '<', '>', ',', ':', ';', '-', '+', '*', '/', '=', '^',
    '&', '|'
]


class Stack():
    def __init__(self) -> None:
        self.__buffer = []

    def pop(self) -> Any:
        self.__buffer.pop()

    def push(self, elemt) -> Any:
        self.__buffer.append(elemt)

    def __len__(self):
        return len(self.__buffer)


class Queue():
    def __init__(self) -> None:
        self.__buffer = []

    def pop(self) -> Any:
        self.__buffer.pop(0)

    def push(self, elemt) -> Any:
        self.__buffer.append(elemt)

    def __len__(self):
        return len(self.__buffer)


def readFile(filePath: str) -> str:
    lines = ""
    with open(filePath) as file:
        for line in file:
            lines = lines + line
    return lines


def searchIfElse(data: list) -> None:
    return None


def searchSwitch(data: list[str],
                 caseNum: list,
                 switcTimes: int = 0,
                 status=False) -> int:
    index = 0
    stack = Stack()
    num = 0
    flag = False
    while index < len(data):
        if data[index] == 'switch' and flag is False:
            flag = True
            switcTimes += 1
        elif data[index] == 'case' and flag is True:
            num += 1
        elif data[index] == '{' and flag is True:
            stack.push('{')
        elif data[index] == '}' and flag is True:
            stack.pop()
            if len(stack) == 0:
                caseNum.append(str(switcTimes) + ' ' + str(num))
                num = 0
                flag = False
                switcTimes += 1
                if status is True:
                    return index
                else:
                    switcTimes += 1
        elif data[index] == 'switch' and flag is True:
            index = searchSwitch(data[index:], caseNum, switcTimes,
                                 True) + index
        index += 1
    caseNum.sort()
    return index


if __name__ == '__main__':
    # filePath = sys.argv[1]
    start = time.time()
    string = readFile("C://vscode//.vscode//plane.cpp")
    string = re.sub(r'\".*\"', '', string)
    string = re.sub(r"//.*", '', string)
    string = string.replace('\n', '')
    string = re.sub(r'/\*.*\*/', '', string)
    # print(string)
    for i in BRACKETS:
        string = string.replace(i, ' ' + i + ' ')
    # print(string)
    key_dic = {}
    for i in KEY_WORD:
        key_dic[i] = 0
    string = string.split(' ')
    for i in string:
        try:
            key_dic[i] += 1
        except Exception:
            continue
    num = 0
    for value in key_dic.values():
        num += value
    while True:
        try:
            string.remove('')
        except Exception:
            break
    print(key_dic)
    print(num)
    caseNum = []
    searchSwitch(string, caseNum)
    print(caseNum)
    print(time.time() - start)
