# -*-coding:utf-8-*-
import sys
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
    lines = lines.split(' ')
    while True:
        try:
            lines.remove('')
        except Exception:
            break
    return lines


def searchIfElse(data: list[str],
                 ifDic: dict,
                 status=False,
                 rightBrackets=Stack()) -> int:
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
                index = searchIfElse(data[:index + 1], ifDic, True,
                                     rightBrackets)
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


def searchKeyWords(data: list[str]) -> int:
    index = -1
    while index < len(data):
        index += 1
        try:
            keyDic[data[index]] += 1
            if data[index] == 'if':
                if data[index - 1] == 'else':
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
    level = 1
    if len(sys.argv) == 3:
        path = sys.argv[1]
        level = int(sys.argv[2])
    start = time.time()
    string = readFile(path)
    keyDic = {}
    for i in KEY_WORD:
        keyDic[i] = 0
    if level >= 1:
        num = searchKeyWords(string)
        print('total num: ' + str(num))
    if level >= 2:
        caseNum = []
        searchSwitch(string, caseNum)
        print('switch num: ' + str(len(caseNum)))
        print('case num: ', end='')
        for i in caseNum:
            print(i[2:], end=' ')
        print()
    if level > 2:
        ifDic = {0: 0, 1: 0}
        searchIfElse(string, ifDic)
        if level >= 3:
            print('if-else num: ' + str(ifDic[0]))
        print('if-elseif-else num: ' + str(ifDic[1]))
    print(time.time() - start)
