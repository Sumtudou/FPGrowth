# -*- coding:utf-8 -*-
# @Time: 2020/4/8 10:31
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: xlsxReadLevel3.py
import csv
import re
import os
import xlrd
import xlwt
import mysqlForFpGrowth
from mysqlForFpGrowth import *


def readXlsxFromLevel3():
    current_path = os.getcwd()
    path = current_path + '/file/level1-3 revised by zhao.xlsx'
    # print(path)
    readbook = xlrd.open_workbook(path)

    worksheet = readbook.sheet_by_name("level3")
    # print(worksheet)
    nrows = worksheet.nrows  # 获取该表总行数
    ncols = worksheet.ncols  # 获取该表总列数
    keySet = set()
    for i in range(1, nrows - 1):  # 去掉首行的表头和结尾的unsure
        # print(worksheet.row_values(i))  # 以列表形式读出，列表中的每一项是str类型
        item = worksheet.row_values(i)
        # print(item[4])
        res = re.split("!!|&&|=", item[4])
        # print(res)
        for i in range(0, len(res), 2):
            keySet.add(res[i])
        # print(keySet)

    theSql = "select * from osm_tag where "
    first = True
    for item in keySet:
        str1 = "tagkey = '" + item + "' "
        if (first):
            theSql = theSql + str1
            first = False
        else:
            theSql = theSql + "OR " + str1
    print(theSql)
    return theSql


# 获得最终结果的数字排序 ， 得到想要的数据
def getTheLastRes():
    allKeySet, allValueSet, fatherSet = mysqlForFpGrowth.level3ToAllTag()
    lenAllKeySet = len(allKeySet)
    # for i in range(0,100):
    #     print(keySet[i],"   ",valueSet[i])

    current_path = os.getcwd()
    path = current_path + '/file/level1-3 revised by zhao.xlsx'
    if not os.path.exists(current_path + "/log/levelOut"):
        os.mkdir(current_path + "/log/levelOut")

    save_path1 = current_path + "/log/levelOut/sum++.txt"
    save_path2 = current_path + "/log/levelOut/res.txt"

    f1 = open(save_path1, "w")
    f2 = open(save_path2, "w")

    readbook = xlrd.open_workbook(path)
    worksheet = readbook.sheet_by_name("level3")
    nrows = worksheet.nrows  # 获取该表总行数
    ncols = worksheet.ncols  # 获取该表总列数
    keySet = []
    valueSet = []
    sum = 0
    ANS = {}  # 结果集
    no = 1  # 序号
    for i in range(1, nrows - 1):  # 去掉首行的表头和结尾的unsure   (1, nrows - 1)

        keySet.clear()
        valueSet.clear()
        sum = 0
        item = worksheet.row_values(i)
        # print(item)
        # print(item[4])
        if '!!' in item[4]:
            type = "||"
        else:
            type = "&&"

        # 分割处理key，value拼接成那个数组
        res = re.split("!!|&&|=", item[4])
        for i in range(0, len(res), 2):
            keySet.append(res[i])
        for i in range(1, len(res), 2):
            valueSet.append(res[i])
        # print("keySet:", keySet, "   valueSet:", valueSet, "  type:", type)

        if type == "&&":  # &&的情况，开始操作zb了
            for j in range(lenAllKeySet):
                # print("allkeySet:", allKeySet[j], "   allvalueSet:", allValueSet[j])

                if set(keySet) <= set(allKeySet[j]) and set(valueSet) <= set(allValueSet[j]):
                    # print (("sum++","keySet:", keySet, "   valueSet:", valueSet,
                    #      "  allkeyset:", allKeySet[j],"  allvalueset:", allValueSet[j]),file = f)
                    sum = sum + 1

                # if j == 100:
                #     break
        else:  # || 的情况了
            # 写的有点迷糊了，下面二重循环，第一层是22W条tag数据，二层是相或的tag，value ，set，只要有一组数据在第一层出现，即可sum++ ，并跳出
            # print("keySet:", keySet, "   valueSet:", valueSet, "  type:", type)
            lenKeySet = len(keySet)
            for j in range(lenAllKeySet):

                for k in range(lenKeySet):  # K  keySet: ['aeroway', 'military']
                                            # valueSet: ['airfield', 'airfield']   type: ||
                    if keySet[k] in allKeySet[j] and valueSet[k] in allValueSet[j]:
                        sum = sum + 1
                        break
        # print("sum="+sum+"\tres=",res)
        # print(("no = {:<6}  sum = {:<10} item = [{}]".format(no, sum, item[4])), file=f2)
        # no += 1
        #ggg1 = item[4]
        ANS[item[4]] = sum
    print("solve over")
    saveToCsvHeader()
    for key in sorted(ANS, key=ANS.__getitem__, reverse=True):
        theItem = []
        theItem.append(no)
        theItem.append(ANS[key])
        theItem.append(key)

        saveTocsv(theItem)
        theItem.clear()
        #print(("no = {:<6}  sum = {:<10} item = [{}]".format(no, ANS[key], key)), file=f2)
        no += 1
    print("print over")

def saveTocsv(data):
    with open('log/csv/res.csv', 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    #保存到CSV的头部
def saveToCsvHeader():
    header = ['no','sum','item']
    with open('log/csv/res.csv', 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

if __name__ == '__main__':
    getTheLastRes()
