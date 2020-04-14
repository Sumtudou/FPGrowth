# -*- coding:utf-8 -*-
# @Time: 2020/4/12 10:34
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: classification.py

# 解决关于分类挖掘的问题。

from FpTemplate import *
from fp_growth import *
import pymysql
import csv
import re
from tkinter import _flatten

# 共用部分，链接数据库
#########我是分割线线线###########
USERNAME = "root"
PASSWD = "123456"
ADDR = "localhost"
DATABASE = "osm"
db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
cursor = db.cursor()


#########我是分割线线线###########


# 或得频次高的 类
def getItemFromCsv():
    itemSet = []
    i = 0
    with open('log/csv/res.csv', 'r') as f:
        reader = csv.reader(f)
        # print(type(reader))

        for row in reader:
            if i > 0 and i < 21:
                itemSet.append(row[2])
            i += 1
            # print(row)
    # print("************")
    # for item in itemSet:
    #     print(item)
    return itemSet


def getClassRes():
    sql = "SELECT tagkey ,tagvalue FROM osm_node where tagkey is not null union all" \
          " SELECT tagkey ,tagvalue FROM osm_road where tagkey is not null union all " \
          "SELECT tagkey ,tagvalue FROM osm_relation where tagkey is not null ;"
    cursor.execute(sql)
    results = cursor.fetchall()

    # 原始数据集：从数据库中取出并处理
    originalKeySet = []
    originalValueSet = []

    # i = 0
    for origin in results:
        keys = origin[0].split(';')
        values = origin[1].split(';')

        keys.pop()  # 去掉结尾为空的元素
        values.pop()

        originalKeySet.append(keys)
        originalValueSet.append(values)

        # print("origin:",origin)
        # print("keys:",keys)
        # print("values:",values)
        # i+=1
        # if i == 10:
        #     break
    # print(originalKeySet)
    # print(originalValueSet)
    itemSet = getItemFromCsv()  # level3中出现度较高的类
    lenOriginalKeySet = len(originalKeySet)

    # 条件的key，value集合，包含需要包含的类如 highway = traffic_signals
    keySet = []
    valueSet = []
    ANS = {}  # 结果集
    no = 1  # 序号
    for item in itemSet:

        # 包含指定的类的结果集
        resKeySet = []
        resValueSet = []

        keySet.clear()
        valueSet.clear()
        # print(item)
        if '!!' in item:
            type = "||"
        else:
            type = "&&"

        # 分割处理key，value拼接成那个数组
        res = re.split("!!|&&|=", item)
        for i in range(0, len(res), 2):
            keySet.append(res[i])
        for i in range(1, len(res), 2):
            valueSet.append(res[i])
        # print("keySet:", keySet, "   valueSet:", valueSet, "  type:", type)

        if type == "&&":  # &&的情况，开始操作zb了
            for j in range(lenOriginalKeySet):
                # print("allkeySet:", allKeySet[j], "   allvalueSet:", allValueSet[j])

                if set(keySet) <= set(originalKeySet[j]) and set(valueSet) <= set(originalValueSet[j]):
                    # print (("sum++","keySet:", keySet, "   valueSet:", valueSet,
                    #      "  allkeyset:", allKeySet[j],"  allvalueset:", allValueSet[j]),file = f)
                    # diffKey：key的差集
                    # diffValue：value的差集
                    diffKey, diffValue = dadKillSon(originalKeySet[j], originalValueSet[j], keySet, valueSet)
                    if len(diffKey) != 0 and len(diffValue) != 0:
                        resKeySet.append(diffKey)
                        resValueSet.append(diffValue)
                    # resKeySet.append(originalKeySet[j])
                    # resValueSet.append(originalValueSet[j])

                # if j == 100:
                #     break
        else:  # || 的情况了
            # 写的有点迷糊了，下面二重循环，第一层是22W条tag数据，二层是相或的tag，value ，set，只要有一组数据在第一层出现，即可sum++ ，并跳出
            # print("keySet:", keySet, "   valueSet:", valueSet, "  type:", type)
            lenKeySet = len(keySet)
            for j in range(lenOriginalKeySet):

                for k in range(lenKeySet):  # K  keySet: ['aeroway', 'military']
                    # valueSet: ['airfield', 'airfield']   type: ||
                    if keySet[k] in originalKeySet[j] and valueSet[k] in originalValueSet[j]:
                        # diffKey：key的差集
                        # diffValue：value的差集
                        diffKey, diffValue = dadKillSon(originalKeySet[j], originalValueSet[j], keySet, valueSet)
                        if len(diffKey) != 0 and len(diffValue) != 0:
                            resKeySet.append(diffKey)
                            resValueSet.append(diffValue)
                        # resKeySet.append(originalKeySet[j])
                        # resValueSet.append(originalValueSet[j])
                        break
        getResTxt(resKeySet, resValueSet, item, no)
        no += 1
        # print(len(resKeySet))
        # print(item)
        # print("resKey",resKeySet)
        # print(list(_flatten(resKeySet)))
        # for i in range(len(resKeySet)):
        #     print(resKeySet[i],"   ",resValueSet[i])
        # break
    print("success!")


# 计算差集，res = dad - son
def dadKillSon(dadKey, dadValue, sonKey, sonValue):
    flag = "WILLBEKILL"
    lenDad = len(dadKey)
    lenSon = len(sonKey)
    for i in range(lenDad):
        for j in range(lenSon):
            if dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]:
                dadKey[i] = flag
                dadValue[i] = flag
                break

    # print(dadKey)
    # print(dadValue)
    keys = list(filter(lambda x: x != flag, dadKey))
    values = list(filter(lambda x: x != flag, dadValue))
    return keys, values


def getResTxt(resKeySet, resValueSet, name, no):
    print("sssss")
    print(len(resKeySet))
    print(len(resValueSet))
    if no == 15:
        for i in resValueSet:
            print(i)
    newName = 'classRes/' + str(no) + '-' + name + '###'
    getFpGrowthRes(resKeySet, newName + 'KEY', 0.05, 0.75)  # key的关联
    getFpGrowthRes(resValueSet, newName + 'VALUE', 0.05, 0.75)  # value的关联

    keys = list(_flatten(resKeySet))  # 直接转一维的
    values = list(_flatten(resValueSet))
    lens = len(keys)
    lenv = len(values)

    print("ggg", lens, lenv)
    kv = []
    for i in range(lens):
        item = []
        item.append(keys[i])
        item.append(values[i])
        kv.append(item)
    # for ggg in kv:
    #     print(ggg)
    getFpGrowthRes(kv, newName + 'KV', 0.05, 0.75)  # KV


if __name__ == '__main__':
    getClassRes()
