# -*- coding:utf-8 -*-
# @Time: 2020/6/7 12:39
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: spare.py
# 一些闲置的文件

# def getResTxt(resKeySet, resValueSet, name, no):
#     global data_length
#     print("数据长度key", len(resKeySet))
#     print("数据长度value", len(resValueSet))
#     newName = 'classRes/' + str(no) + '-' + name + '###'
#     # for i in range(0,30):
#     #     print("keySet和valueSet")
#     #     print(resKeySet[i],"   ",resValueSet[i])
#     # 每一个tag的key和value的集合
# keyAndValue = []
# lenRes = len(resKeySet)  #二维列表的第一维长度
# for i in range(lenRes):
#     itemList = []
#     for j in range(len(resKeySet[i])):
#         item = resKeySet[i][j] + "=" + resValueSet[i][j]
#         itemList.append(item)
#     keyAndValue.append(itemList)
#
#     keys = list(_flatten(resKeySet))  # 直接转一维的
#     values = list(_flatten(resValueSet))
#     lens = len(keys)
#     lenv = len(values)
#
#     # print("ggg", lens, lenv)
#     kv = []
#     for i in range(lens):
#         item = []
#         item.append(keys[i])
#         item.append(values[i])
#         kv.append(item)
#
#     f1Over = f2Over = f3Over = f4Over = False
#
#     for i in range(0, 25):  # 0 1 2 3
#         step = i * 0.01
#         min_sup = 0.25 - step
#         min_conf = 0.95 - step
#         # len1 = len2 = len3 = len4 = -1
#         # rule1 = rule2 = rule3 = rule4 = -1
#         print("minsup", min_sup, "  minconf", min_conf)
#         if not f1Over:
#             len1, rule1, data_length1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)  # KV
#         if not f2Over:
#             len2, rule2, data_length2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)  # key的关联
#         if not f3Over:
#             len3, rule3, data_length3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)  # value的关联
#         if not f4Over:
#             len4, rule4, data_length4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup,
#                                                        min_conf)  # 每一个tag内部关联
#
#         if (len1 > 10 and not f1Over) or (i == 24 and not f1Over):
#             f1Over = True
#             if len1 != 0:
#                 for item in rule1:
#                     min_sup_num = int(math.floor(data_length1 * min_sup))
#                     support = calSupport(list(item[0]), list(item[1]), kv)
#                     saveRuleToMysql(data_length1, min_sup, min_conf, min_sup_num,
#                                     item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KV", support)
#             else:  # 长度为零，就是空的规则返回去了
#                 min_sup_num = int(math.floor(data_length1 * min_sup))
#                 saveRuleToMysql(data_length1, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KV", 0.0)
#
#         if (len2 > 10 and not f2Over) or (i == 24 and not f2Over):
#             f2Over = True
#             if len2 != 0:
#                 for item in rule2:
#                     min_sup_num = int(math.floor(data_length2 * min_sup))
#                     support = calSupport(list(item[0]), list(item[1]), resKeySet)
#                     saveRuleToMysql(data_length2, min_sup, min_conf, min_sup_num,
#                                     item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KEY", support)
#             else:
#                 min_sup_num = int(math.floor(data_length2 * min_sup))
#                 saveRuleToMysql(data_length2, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KEY", 0.0)
#
#         if (len3 > 10 and not f3Over) or (i == 24 and not f3Over):
#             f3Over = True
#             if len3 != 0:
#                 for item in rule3:
#                     min_sup_num = int(math.floor(data_length3 * min_sup))
#                     support = calSupport(list(item[0]), list(item[1]), resValueSet)
#
#                     saveRuleToMysql(data_length3, min_sup, min_conf, min_sup_num,
#                                     item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "VALUE",
#                                     support)
#             else:
#                 min_sup_num = int(math.floor(data_length3 * min_sup))
#                 saveRuleToMysql(data_length3, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "VALUE", 0.0)
#
#         if (len4 > 10 and not f4Over) or (i == 24 and not f4Over):
#             f4Over = True
#             if len4 != 0:
#                 for item in rule4:
#                     min_sup_num = int(math.floor(data_length4 * min_sup))
#                     support = calSupport(list(item[0]), list(item[1]), keyAndValue)
#
#                     saveRuleToMysql(data_length4, min_sup, min_conf, min_sup_num,
#                                     item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "TAGINSIDE",
#                                     support)
#             else:
#                 min_sup_num = int(math.floor(data_length4 * min_sup))
#                 saveRuleToMysql(data_length4, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "TAGINSIDE", 0.0)
#
#
#
# # 计算差集，res = dad - son ，并剔除黑名单的key
# # 传入的都是一维数组了
# # 第一种处理方式，就是把包含的类都去掉 例如 [k1,v1]
# # 那么对于   [k1] [v1],   [k1,k2] [v1,v2] 得到 [k2,v2]
# def dadKillSon(dadKey, dadValue, sonKey, sonValue):
#     # print("dadKey ",dadKey)
#     # print("dadValue ",dadValue)
#     # print("sonKey ",sonKey)
#     # print("sonValue ",sonValue)
#     # print(len(dadKey)," ",len(sonKey))
#     flag = "WILLBEKILL"
#     lenDad = len(dadKey)
#     lenSon = len(sonKey)
#     for i in range(lenDad):
#         fs = False
#         for j in range(lenSon):  # 去掉分类的tag对
#             if dadKey[i] == sonKey[j] and dadValue[i] == sonValue[j]:
#                 dadKey[i] = flag
#                 dadValue[i] = flag
#                 # print("haskilld")
#                 fs = True
#                 break
#
#         if fs == False:  # 去掉黑名单的tag对
#             for iter in blackList:
#                 if iter in dadKey[i]:
#                     dadKey[i] = flag
#                     dadValue[i] = flag
#                     break
#
#     keys = list(filter(lambda x: x != flag, dadKey))
#     values = list(filter(lambda x: x != flag, dadValue))
#
#     # print("返回前",keys)
#     # print("返回前",values)
#
#     return keys, values

# for key in sorted(ANS, key=ANS.__getitem__, reverse=True):
#     theItem = []
#     theItem.append(no)        #序号
#     theItem.append(ANS[key])  #出现的次数
#     theItem.append(key)       #名称
#     saveTocsv(theItem)
#     theItem.clear()
#     no += 1
# #保存到csv文件
# def saveTocsv(data):
#     with open('log/csv/res.csv', 'a+', encoding='utf-8', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(data)
#
#   #以下两个list分别保存类内的key和value
#   resKey= []
#   resValue= []
#   kl = "highway"
#   v1 = "residential"
#   for item in allTags #遍历每一个Tag
#       if k1 in allTags.key and v1 in allTags.value:
#       resKey.append(allTags.key)
#       resValue.append(allTags.value)
#
#
# # 共用部分，链接数据库
# USERNAME = "root"
# PASSWD = "123456"
# ADDR = "localhost"
# DATABASE = "osm"
# db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
# cursor = db.cursor()
# #将规则保存到数据库中
# def saveRuleToMysql(data_len, min_sup, min_conf, min_sup_num,
#                     confidence, first, second, name, no, type,support):
#
#     saveSql = "insert into osm_rule (data_len,min_sup,min_conf,min_sup_num," \
#               "confidence,first,second,name,no,type,status,support)" \
#               " values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')"\
#         .format(data_len, min_sup, min_conf, min_sup_num, confidence, first, second, name, no, type,1,support)
#     print(saveSql)
#     try:
#         cursor.execute(saveSql)
#         db.commit()
#     except:
#         db.rollback()