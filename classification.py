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
blackList = ['source','name']  # ,'ref', 'type' ,'name',

topNum = 5  # 出现频次前  num 次的类


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
    # ifFirst  = True
    for origin in results:
        keys = origin[0].split(';')
        values = origin[1].split(';')

        keys.pop()  # 去掉结尾为空的元素
        values.pop()

        # print("origin:",origin)
        # print("keys:",keys)
        # print("values:",values)
        originalKeySet.append(keys)
        originalValueSet.append(values)
        # print("originalKeySet:",originalKeySet)
        # print("originalValueSet",originalValueSet)
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
                #这里有巨大的bug，可能这个key和value不对应啊啊啊 比如proposed既可以是key还可以是value   2020.5.8修改
                #因为这里前五的类keySet和valueSet都只有一个数值。这里简化操作啊啊啊，后来者要谨慎
                if set(keySet) <= set(originalKeySet[j]) and set(valueSet) <= set(originalValueSet[j]):
                    for jj in range(len(originalKeySet[j])):
                        if keySet[0] == originalKeySet[j][jj] and valueSet[0] == originalValueSet[j][jj]:
                            diffKey, diffValue = dadKillSon2(originalKeySet[j], originalValueSet[j], keySet, valueSet)
                            if len(diffKey) != 0 and len(diffValue) != 0:
                                resKeySet.append(diffKey)
                                resValueSet.append(diffValue)
                    # print (("sum++","keySet:", keySet, "   valueSet:", valueSet,
                    #      "  allkeyset:", allKeySet[j],"  allvalueset:", allValueSet[j]),file = f)
                    # diffKey：key的差集
                    # diffValue：value的差集

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
                        diffKey, diffValue = dadKillSon2(originalKeySet[j], originalValueSet[j], keySet, valueSet)
                        if len(diffKey) != 0 and len(diffValue) != 0:
                            # print("会添加")
                            resKeySet.append(diffKey)
                            resValueSet.append(diffValue)
                        # resKeySet.append(originalKeySet[j])
                        # resValueSet.append(originalValueSet[j])
                        break

        # for i in range(len(resKeySet)):
        #     for j in range(len(resKeySet[i])):
        #         if resKeySet[i][j] == "oneway" and resValueSet[i][j] == "yes":
        #             for k in range(len(resKeySet[i])):
        #                 if (resKeySet[i][k] == "highway" and resValueSet[i][k] != "residential") or (resKeySet[i][k] != "highway" and resValueSet[i][k] == "residential"):
        #                     print("resKey",resKeySet[i],"  resValue",resValueSet[i])

        getResTxt3(resKeySet, resValueSet, item, no)
        no += 1
        # print(len(resKeySet))
        # print(item)
        # print("resKey",resKeySet)
        # print(list(_flatten(resKeySet)))
        # for i in range(len(resKeySet)):
        #     print(resKeySet[i],"   ",resValueSet[i])

        #break

    print("success!")




# 计算差集，res = dad - son ，并剔除黑名单的key
# 传入的都是一维数组了
# 第二种处理方式，就是把包含的类都去掉 例如 [k1,v1]
# 那么对于  { [k1] [v1], [k1,k2] [v1,v2]} 得到  {[k1,k2] [v1,v2]}
def dadKillSon2(dadKey, dadValue, sonKey, sonValue):
    # print("dadKey ", dadKey)
    # print("dadValue ", dadValue)
    # print("sonKey ", sonKey)
    # print("sonValue ", sonValue)
    # print(len(dadKey), " ", len(sonKey))
    flag = "WILLBEKILL"
    lenDad = len(dadKey)
    lenSon = len(sonKey)
    for i in range(lenDad):
        fs = False
        for j in range(lenSon):  # 去掉分类的tag对
            if (dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]) and (lenDad == lenSon):  # 因为前五个lenson一定等于1
                dadKey[i] = flag  # 原来的条件是dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]
                dadValue[i] = flag
                # print("haskilld")
                fs = True
                break

        if fs == False:  # 去掉黑名单的tag对
            for iter in blackList:
                if iter in dadKey[i]:
                    dadKey[i] = flag
                    dadValue[i] = flag
                    break

    keys = list(filter(lambda x: x != flag, dadKey))
    values = list(filter(lambda x: x != flag, dadValue))
    # print("一半了 keys:",keys,"  values:",values)
    lenDad = len(keys)
    if len(keys) != 0:
        for i in range(lenDad):
            fs = False
            for j in range(lenSon):  # 去掉分类的tag对
                # print("i:",i," j:",j)
                # print(keys[i],values[i])
                # print(sonKey[j],sonValue[j])
                # print(lenDad,"  ",lenSon)
                if (keys[i] == sonKey[j] and values[i] == sonValue[j]) and (lenDad == lenSon):  # 因为前五个lenson一定等于1
                    # print("再次")
                    keys[i] = flag  # 原来的条件是dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]
                    values[i] = flag
                    fs = True
                    break

            if fs:
                break
        keys1 = list(filter(lambda x: x != flag, keys))
        values1 = list(filter(lambda x: x != flag, values))
        return keys1, values1

    return keys, values


# 第二种解析方式，将置信度和支持度分为5档。每一档都保存。
# 再做对比。

def getResTxt2(resKeySet, resValueSet, name, no):
    global data_length
    print("数据长度key", len(resKeySet))
    print("数据长度value", len(resValueSet))
    newName = 'classRes/' + str(no) + '-' + name + '###'

    keyAndValue = []
    lenRes = len(resKeySet)
    for i in range(lenRes):
        itemList = []
        for j in range(len(resKeySet[i])):
            item = resKeySet[i][j] + "=" + resValueSet[i][j]
            itemList.append(item)
        keyAndValue.append(itemList)

    keys = list(_flatten(resKeySet))  # 直接转一维的
    values = list(_flatten(resValueSet))
    lens = len(keys)
    lenv = len(values)

    # print("ggg", lens, lenv)
    kv = []
    for i in range(lens):
        item = []
        item.append(keys[i])
        item.append(values[i])
        kv.append(item)

    f1Over = f2Over = f3Over = f4Over = False

    for i in range(0, 5):  # 0 1 2 3 4
        step = i * 0.01
        min_sup = i * 0.02 + 0.01
        min_conf = i*0.05 + 0.7
        #min_conf = 1 - 0.05 * (i + 2)
        print("minsup", min_sup, "  minconf", min_conf)

        len1, rule1, data_length1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)  # KV
        len2, rule2, data_length2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)  # key的关联
        len3, rule3, data_length3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)  # value的关联
        len4, rule4, data_length4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup, min_conf)  # 每一个tag内部关联

        if len1 != 0:
            for item in rule1:
                min_sup_num = int(math.floor(data_length1 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), kv)
                saveRuleToMysql2(data_length1, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KV", support,
                                 i + 1)
        else:  # 长度为零，就是空的规则返回去了
            min_sup_num = int(math.floor(data_length1 * min_sup))
            saveRuleToMysql2(data_length1, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KV", 0.0, i + 1)

        if len2 != 0:
            for item in rule2:
                min_sup_num = int(math.floor(data_length2 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), resKeySet)
                saveRuleToMysql2(data_length2, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KEY", support,
                                 i + 1)
        else:
            min_sup_num = int(math.floor(data_length2 * min_sup))
            saveRuleToMysql2(data_length2, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KEY", 0.0, i + 1)

        if len3 != 0:
            for item in rule3:
                min_sup_num = int(math.floor(data_length3 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), resValueSet)

                saveRuleToMysql2(data_length3, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "VALUE", support,
                                 i + 1)
        else:
            min_sup_num = int(math.floor(data_length3 * min_sup))
            saveRuleToMysql2(data_length3, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "VALUE", 0.0, i + 1)

        if len4 != 0:
            for item in rule4:
                min_sup_num = int(math.floor(data_length4 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), keyAndValue)

                saveRuleToMysql2(data_length4, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "TAGINSIDE",
                                 support, i + 1)
        else:
            min_sup_num = int(math.floor(data_length4 * min_sup))
            saveRuleToMysql2(data_length4, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "TAGINSIDE", 0.0,
                             i + 1)

def getResTxt3(resKeySet, resValueSet, name, no):
    global data_length
    print("数据长度key", len(resKeySet))
    print("数据长度value", len(resValueSet))
    newName = 'classRes/' + str(no) + '-' + name + '###'

    keyAndValue = []
    lenRes = len(resKeySet)
    for i in range(lenRes):
        itemList = []
        for j in range(len(resKeySet[i])):
            item = resKeySet[i][j] + "=" + resValueSet[i][j]
            itemList.append(item)
        keyAndValue.append(itemList)

    keys = list(_flatten(resKeySet))  # 直接转一维的
    values = list(_flatten(resValueSet))
    lens = len(keys)
    lenv = len(values)

    # print("ggg", lens, lenv)
    kv = []
    for i in range(lens):
        item = []
        item.append(keys[i])
        item.append(values[i])
        kv.append(item)

    f1Over = f2Over = f3Over = f4Over = False

    for i in range(0, 5):  # 0 1 2 3 4
        step = i * 0.01
        min_sup = i * 0.02 + 0.01
        min_conf = 0.4
        #min_conf = 1 - 0.05 * (i + 2)
        print("minsup", min_sup, "  minconf", min_conf)

        len1, rule1, data_length1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)  # KV
        len2, rule2, data_length2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)  # key的关联
        len3, rule3, data_length3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)  # value的关联
        len4, rule4, data_length4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup, min_conf)  # 每一个tag内部关联

        if len1 != 0:
            for item in rule1:
                min_sup_num = int(math.floor(data_length1 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), kv)
                saveRuleToMysql3(data_length1, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KV", support,
                                 i + 1)
        else:  # 长度为零，就是空的规则返回去了
            min_sup_num = int(math.floor(data_length1 * min_sup))
            saveRuleToMysql3(data_length1, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KV", 0.0, i + 1)

        if len2 != 0:
            for item in rule2:
                min_sup_num = int(math.floor(data_length2 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), resKeySet)
                saveRuleToMysql3(data_length2, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KEY", support,
                                 i + 1)
        else:
            min_sup_num = int(math.floor(data_length2 * min_sup))
            saveRuleToMysql3(data_length2, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KEY", 0.0, i + 1)

        if len3 != 0:
            for item in rule3:
                min_sup_num = int(math.floor(data_length3 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), resValueSet)

                saveRuleToMysql3(data_length3, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "VALUE", support,
                                 i + 1)
        else:
            min_sup_num = int(math.floor(data_length3 * min_sup))
            saveRuleToMysql3(data_length3, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "VALUE", 0.0, i + 1)

        if len4 != 0:
            for item in rule4:
                min_sup_num = int(math.floor(data_length4 * min_sup))
                support = calSupport(list(item[0]), list(item[1]), keyAndValue)

                saveRuleToMysql3(data_length4, min_sup, min_conf, min_sup_num,
                                 item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "TAGINSIDE",
                                 support, i + 1)
        else:
            min_sup_num = int(math.floor(data_length4 * min_sup))
            saveRuleToMysql3(data_length4, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "TAGINSIDE", 0.0,
                             i + 1)


def calSupport(list1, list2, target):
    lists = list1 + list2
    sum = 0
    for item in target:
        if set(lists) <= set(item):
            sum = sum + 1

    return float(sum) / float(len(target))


if __name__ == '__main__':
    #cursor.execute('truncate table osm_rule2')  # 先截断表
    cursor.execute('truncate table osm_rule3')  # 先截断表

    getClassRes()

# 为什么统计的类的次数较大，经常一万多，但是到了分析就只有几百甚至几十？
# 因为去重了，并且还去掉了包含类本身的这个字段。
# 比如highway = residential 有 13000次
# 首先干掉 highway = residential 这个本身，几千个就没了
# 再干掉黑名单内的 tag 对，又去掉了一些。结果数量就大大减少了
