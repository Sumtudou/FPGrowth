# -*- coding:utf-8 -*-
# @Time: 2020/4/12 10:34
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: classification.py

# 解决关于分类挖掘的问题。

from FpTemplate import *
from mysqlForFpGrowth import *
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

####### 原始数据集的key的黑名单 ##########
blackList = ['name', 'type', 'ref']

topNum = 19  # 出现频次前  num 次的类


# 获得频次高的 类
def getItemFromCsv():
    itemSet = []
    i = 0
    with open('log/csv/res.csv', 'r') as f:
        reader = csv.reader(f)
        # print(type(reader))

        for row in reader:
            if i > 0 and i < topNum + 1:
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


# 计算差集，res = dad - son ，并剔除黑名单的key
def dadKillSon(dadKey, dadValue, sonKey, sonValue):
    flag = "WILLBEKILL"
    lenDad = len(dadKey)
    lenSon = len(sonKey)
    for i in range(lenDad):
        fs = False
        for j in range(lenSon):  # 去掉分类的tag对
            if dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]:
                dadKey[i] = flag
                dadValue[i] = flag
                fs = True
                break

        if fs == False:  # 去掉黑名单的tag对
            for iter in blackList:
                if iter in dadKey[i]:
                    dadKey[i] = flag
                    dadValue[i] = flag
                    break

    # print(dadKey)
    # print(dadValue)
    keys = list(filter(lambda x: x != flag, dadKey))
    values = list(filter(lambda x: x != flag, dadValue))
    return keys, values


def getResTxt(resKeySet, resValueSet, name, no):
    global data_length
    print("数据长度key", len(resKeySet))
    print("数据长度value", len(resValueSet))
    newName = 'classRes/' + str(no) + '-' + name + '###'

    # for i in range(0,30):
    #     print(resKeySet[i],"   ",resValueSet[i])
    # 每一个tag的key和value的集合
    keyAndValue = []
    lenRes = len(resKeySet)
    for i in range(lenRes):
        itor = []
        itor.append(resKeySet[i] + resValueSet[i])  # key在前，value在后
        keyAndValue.append(itor[0])
    # print("keyAndValue")
    # print(keyAndValue)

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

    f1Over = f2Over = f3Over = f4Over = False

    for i in range(0, 10):  # 0 1 2 3
        step = i * 0.025
        min_sup = 0.25 - step
        min_conf = 0.95 - step
        #len1 = len2 = len3 = len4 = -1
        #rule1 = rule2 = rule3 = rule4 = -1
        print("minsup", min_sup, "  minconf", min_conf)
        if not f1Over:
            len1, rule1, data_length1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)  # KV
        if not f2Over:
            len2, rule2, data_length2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)  # key的关联
        if not f3Over:
            len3, rule3, data_length3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)  # value的关联
        if not f4Over:
            len4, rule4, data_length4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup,
                                                       min_conf)  # 每一个tag内部关联

        if (len1 > 10 and not f1Over) or (i == 9 and not f1Over):
            f1Over = True
            if len1 != 0:
                for item in rule1:
                    min_sup_num = int(math.floor(data_length1 * min_sup))
                    saveRuleToMysql(data_length1, min_sup, min_conf, min_sup_num,
                                    item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KV")
            else:   #长度为零，就是空的规则返回去了
                min_sup_num = int(math.floor(data_length1 * min_sup))
                saveRuleToMysql(data_length1, min_sup, min_conf, min_sup_num,0.0, "无", "无", name, no, "KV")

        if (len2 > 10 and not f2Over) or (i == 9 and not f2Over):
            f2Over = True
            if len2 != 0:
                for item in rule2:
                    min_sup_num = int(math.floor(data_length2 * min_sup))
                    saveRuleToMysql(data_length2, min_sup, min_conf, min_sup_num,
                                    item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KEY")
            else:
                min_sup_num = int(math.floor(data_length2 * min_sup))
                saveRuleToMysql(data_length2, min_sup, min_conf, min_sup_num,0.0, "无", "无", name, no, "KEY")

        if (len3 > 10 and not f3Over) or (i == 9 and not f3Over):
            f3Over = True
            if len3 !=0:
                for item in rule3:
                    min_sup_num = int(math.floor(data_length3 * min_sup))
                    saveRuleToMysql(data_length3, min_sup, min_conf, min_sup_num,
                                    item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "VALUE")
            else:
                min_sup_num = int(math.floor(data_length3 * min_sup))
                saveRuleToMysql(data_length3, min_sup, min_conf, min_sup_num,0.0, "无", "无", name, no, "VALUE")

        if (len4 > 10 and not f4Over) or (i == 9 and not f4Over):
            f4Over = True
            if len4 != 0:
                for item in rule4:
                    min_sup_num = int(math.floor(data_length4 * min_sup))
                    saveRuleToMysql(data_length4, min_sup, min_conf, min_sup_num,
                                    item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "TAGINSIDE")
            else:
                min_sup_num = int(math.floor(data_length4 * min_sup))
                saveRuleToMysql(data_length4, min_sup, min_conf, min_sup_num,0.0, "无", "无", name, no, "TAGINSIDE")

if __name__ == '__main__':
    cursor.execute('truncate table osm_rule')  # 先截断表
    getClassRes()

# 为什么统计的类的次数较大，经常一万多，但是到了分析就只有几百甚至几十？
# 因为去重了，并且还去掉了包含类本身的这个字段。
# 比如highway = residential 有 13000次
# 首先干掉 highway = residential 这个本身，几千个就没了
# 再干掉黑名单内的 tag 对，又去掉了一些。结果数量就大大减少了
