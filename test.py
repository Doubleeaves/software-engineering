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

    def top(self) -> Any:
        return self.__buffer[len(self.__buffer) - 1]


def readFile(filePath: str) -> list[str]:
    lines = ""
    with open(filePath) as file:
        for line in file:
            line.encode('utf-8')
            lines = lines + line
    lines = re.sub(r'\".*\"', '', lines)
    lines = re.sub(r"//.*", '', lines)
    lines = lines.replace('\n', '')
    lines = re.sub(r'/\*.*?\*/', '', lines)
    for i in BRACKETS:
        lines = lines.replace(i, ' ' + i + ' ')
    return lines


def searchIfElse(data: list[str], ifDic: dict, status=False, rightBrackets=Stack()) -> int:
    index = len(data) - 1
    flag = False
    ifType = 0
    stackCount = 0
    while index >= 0:
        if data[index] == 'else':
            if flag is False:
                flag = True
                stackCount = len(rightBrackets)
            else:
                index = searchIfElse(data[:index+1], ifDic, True, rightBrackets)
        elif data[index] == 'if':
            if flag is True and len(rightBrackets) == stackCount:
                ifDic[ifType] += 1
                flag = False
                if status is True:
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
    string = readFile("C://vscode//.vscode//1.cpp")
    for i in BRACKETS:
        string = string.replace(i, ' ' + i + ' ')
    keyDic = {}
    for i in KEY_WORD:
        keyDic[i] = 0
    string = string.split(' ')
    while True:
        try:
            string.remove('')
        except Exception:
            break
    index = -1
    while index < len(string):
        index += 1
        try:
            keyDic[string[index]] += 1
            if string[index] == 'if':
                if string[index-1] == 'else':
                    string[index] = 'elif'
                    string.pop(index-1)
                    index -= 1
        except Exception:
            continue
    num = 0
    for value in keyDic.values():
        num += value
    print('total num: ' + str(num))
    caseNum = []
    ifDic = {0: 0, 1: 0}
    searchSwitch(string, caseNum)
    print('switch num: ' + str(len(caseNum)))
    print('case num: ', end='')
    for i in caseNum:
        print(i[2:], end=' ')
    print()
    searchIfElse(string, ifDic)
    print('if-else num: ' + str(ifDic[0]))
    print('if-elseif-else num: ' + str(ifDic[1]))
    print(time.time() - start)
