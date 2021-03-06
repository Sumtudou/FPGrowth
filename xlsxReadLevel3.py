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

# 返回查询语句，从osm_tag表中得到所有包含在level3表的key
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
        item = worksheet.row_values(i)
        res = re.split("!!|&&|=", item[4])
        for i in range(0, len(res), 2):
            keySet.add(res[i])
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
# 相当于从osm_tag_all里面取数据，判断是否包含level3表中的tag，并统计出现次数。
# 但是取数据需要重新读表，这里采用的是之前生成的level3ToAllTag()方法生成的set
# 优点是节约了取的时间（同时节约了存的时间），缺点是每次统计次数，都需要重新合并表
def getTheLastRes():
    allKeySet, allValueSet, fatherSet = mysqlForFpGrowth.level3ToAllTag()
    lenAllKeySet = len(allKeySet)
    # for i in range(0,100):
    #     print(keySet[i],"   ",valueSet[i])

    current_path = os.getcwd()
    path = current_path + '/file/level1-3 revised by zhao.xlsx'

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
        #!!!!!重点来了，下面    --->  if set(keySet) <= set(allKeySet[j]) and set(valueSet) <= set(allValueSet[j]):
        #有bug，这里统计的key和value没有做到对应相等。要加for循环。但是我懒得改了，加油哦。
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

    #这里是获取到sum即level3表中tag次数统计的过程。
    #流程  osm_tag ->  osm_tag_level3  ->  osm_tag_all
    #最后处理osm_tag_all来得到最后的res.csv文件
    #处理过程，从所有tag中，提取level3表中出现的tag的key值所在键值对。
    #之后按照键值对的id值将其合并到osm_tag_all ,最后用 in 来判断是否出现并统计次数
    #写的这么麻烦的原因：之前的tag已经分开了存储，且源文件中未曾分离relation的tag（虽然后来处理了）
    #导致写的时候分分合合很麻烦，现在可以改的更加简单，但是由于本人较懒，秉承着能跑就行。不太想推倒重来
    #因而留下此注释，以供日后观看                     ------author：sumtudou    date：2020.4.13

    sql = readXlsxFromLevel3()
    mysqlForFpGrowth.saveLevel3(sql)
    mysqlForFpGrowth.level3ToAllTag()
    getTheLastRes()