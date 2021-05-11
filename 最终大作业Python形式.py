import random
from random import choice
import matplotlib.pyplot as plt

P0 = 5
P = 7
Pc = 0.6
Pm = 0.2
Gen = 20
Dict = {0: '0000', 1: '0001', 2: '0010', 3: '0011', 4: '0100', 5: '0101', 6: '0110', 7: '0111', 8: '1000', 9: '1001'}
BinDict = {'0000': 0, '0001': 1, '0010': 2, '0011': 3, '0100': 4, '0101': 5, '0110': 6, '0111': 7, '1000': 8, '1001': 9}
XList = []  # 用来存放P0个元素的数据
rate = []  # 存放每次迭代最小值


def x_y(x):
    y = round((x - 2) * (x - 2), 4)
    return y


while len(XList) < P0:  # 生成P0个随机数
    t = random.uniform(1, 4)
    t = round(t, 2)
    if t not in XList:
        XList.append(t)


def bin_float(binstr):
    Str1 = binstr[0:4]
    Str2 = binstr[4:8]
    Str3 = binstr[8:12]
    if Str1 in BinDict and Str2 in BinDict and Str3 in BinDict:
        data = BinDict[Str1] + BinDict[Str2] * 0.1 + BinDict[Str3] * 0.01
        return data
    else:
        return False


def float_bin(list1):  # 交叉操作：传入P0长度的浮点数列表，输出交叉后的P长度的浮点数列表
    while len(list1) <= P:
        BinList = []  # 存放二进制字符串组成的数组
        for x in list1:
            x = round(x * 100)
            a1 = x % 10
            b1 = (round((x - a1) / 10)) % 10
            c1 = round((x - 10 * b1 - a1) / 100)
            BinList.append(Dict[c1] + Dict[b1] + Dict[a1])
        OverLap = []  # 存放需要参与交叉操作的二进制字符串数组的下标
        while len(OverLap) < round(Pc * P0):
            i = round(random.uniform(0, P0 - 1))
            if i not in OverLap:
                OverLap.append(i)
        OverLapList = []  # 用于存放需要进行交叉的数据
        for i in range(0, round(Pc * P0)):
            OverLapList.append(BinList[OverLap[i]])
        NewOverLapList = []  # 存放需要已由字符串转化为列表的需要交叉的数据组成的列表
        for x in OverLapList:  # 将用于交叉的数据转化为可进行替换操作的列表
            TempList = []
            for i in x:
                if i == '1':
                    TempList.append(1)
                elif i == '0':
                    TempList.append(0)
            NewOverLapList.append(TempList)
        for i in range(0, round(Pc * P0), 2):  # 完成交叉操作
            if round(Pc * P0) % 2 == 1:
                i = 0
            DifList = []  # 存放两相邻待处理二维数字数组不同的位置组成的列表
            for atom in range(0, 12):
                if NewOverLapList[i][atom] != NewOverLapList[i + 1][atom]:
                    DifList.append(atom)
            if len(DifList) != 0:
                r = choice(DifList)
                NewOverLapList[i][r] = (NewOverLapList[i][r] + 1) % 2
                NewOverLapList[i + 1][r] = (NewOverLapList[i + 1][r] + 1) % 2

        for x in NewOverLapList:  # 将用于交叉的数据转化为可进行替换操作的列表
            TempList = []
            NewStr = ''
            for i in x:
                if i == 1:
                    TempList.append('1')
                else:
                    TempList.append('0')
            for i in TempList:
                NewStr += i
            if bin_float(NewStr):
                data = round(bin_float(NewStr), 2)
                if data not in list1:
                    list1.append(data)

    return list1[0:P]


def compare(list5):  # 输入P长度的列表，完成选择操作，选出最适合的P0个
    miny = 10
    for a1 in range(0, len(list5)):
        if x_y(list5[a1]) < miny:
            miny = x_y(list5[a1])
    rate.append(miny)
    while len(list5) > P0:
        maxy = 0
        max1 = 0
        for a1 in range(0, len(list5)):
            if x_y(list5[a1]) >= maxy:
                maxy = x_y(list5[a1])
                max1 = a1
        del (list5[max1])
    return list5


def variation(list2):  # 传入变异前数组，输出变异后数组
    list3 = []
    BinList = []  # 将浮点数转化为二进制字符串组成的列表
    for x in list2:
        x = round(x * 100)
        a1 = x % 10
        b1 = (round((x - a1) / 10)) % 10
        c1 = round((x - 10 * b1 - a1) / 100)
        BinList.append(Dict[c1] + Dict[b1] + Dict[a1])
    OverLap = []  # 存放需要参与变异操作的二进制字符串数组的下标
    OverLapList = []
    while len(OverLap) < round(P0 * Pm):
        i = round(random.uniform(0, P0 - 1))
        if i not in OverLap:
            OverLap.append(i)
    if len(OverLap) > 1:  # 讨论若变异的数目为奇数的情况
        if round(OverLap[0]) > round(OverLap[1]):
            del list2[round(OverLap[0])], list2[round(OverLap[1])]
        else:
            del list2[round(OverLap[1])], list2[round(OverLap[0])]
        OverLapList = []  # 用于存放需要进行变异的数据
        for i in range(round(P0 * Pm)):
            OverLapList.append(BinList[OverLap[i]])
    else:
        OverLapList.append(BinList[OverLap[0]])
    NewOverLapList = []  # 存放需要已由字符串转化为列表的需要变异的数据组成的列表
    for x in OverLapList:  # 将用于变异的数据转化为可进行替换操作的列表
        TempList = []
        for i in x:
            if i == '1':
                TempList.append(1)
            else:
                TempList.append(0)
        NewOverLapList.append(TempList)

    while len(list3) < 2:
        for i in range(0, round(Pm * P0)):
            ran = round(random.uniform(0, 11))
            NewOverLapList[i][ran] = (NewOverLapList[i][ran] + 1) % 2
        for x in NewOverLapList:  # 将用于变异的数据转化为字符串
            TempList = []
            NewStr = ''
            for i in x:
                if i == 1:
                    TempList.append('1')
                else:
                    TempList.append('0')
            for i2 in TempList:
                NewStr += i2
            if bin_float(NewStr):
                data = round(bin_float(NewStr), 2)
                list3.append(data)
    list2 += list3
    return list2


Begin = XList[:]
for i in range(0, Gen, 1):
    data = variation(compare(float_bin(Begin)))
    Begin = data[:]
print(rate)
LineX = range(1, Gen + 1, 1)
plt.plot(LineX, rate)
plt.show()
