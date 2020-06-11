# # -*- coding:utf-8 -*-
# # @Time: 2020/6/7 16:02
# # @Author: sumtudou
# # @Email: sumtudou98@gmail.com
# # @File: test.py
#
# ######
# def getResTxt3(resKeySet, resValueSet, name, no):
#     global data_length
#     print("数据长度key", len(resKeySet))
#     print("数据长度value", len(resValueSet))
#     newName = 'classRes/' + str(no) + '-' + name + '###'
#
#     keyAndValue = []
#     lenRes = len(resKeySet)
#     for i in range(lenRes):
#         itemList = []
#         for j in range(len(resKeySet[i])):
#             item = resKeySet[i][j] + "=" + resValueSet[i][j]
#             itemList.append(item)
#         keyAndValue.append(itemList)
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
#     for i in range(0, 5):  # 0 1 2 3 4
#         step = i * 0.01
#         min_sup = i * 0.02 + 0.01
#         min_conf =  0.7
#         #min_conf = 1 - 0.05 * (i + 2)
#         print("minsup", min_sup, "  minconf", min_conf)
#
#         len1, rule1, data_length1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)  # KV
#         len2, rule2, data_length2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)  # key的关联
#         len3, rule3, data_length3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)  # value的关联
#         len4, rule4, data_length4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup, min_conf)  # 每一个tag内部关联
#
#         if len1 != 0:
#             for item in rule1:
#                 min_sup_num = int(math.floor(data_length1 * min_sup))
#                 support = calSupport(list(item[0]), list(item[1]), kv)
#                 saveRuleToMysql3(data_length1, min_sup, min_conf, min_sup_num,
#                                  item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KV", support,
#                                  i + 1)
#         else:  # 长度为零，就是空的规则返回去了
#             min_sup_num = int(math.floor(data_length1 * min_sup))
#             saveRuleToMysql3(data_length1, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KV", 0.0, i + 1)
#
#         if len2 != 0:
#             for item in rule2:
#                 min_sup_num = int(math.floor(data_length2 * min_sup))
#                 support = calSupport(list(item[0]), list(item[1]), resKeySet)
#                 saveRuleToMysql3(data_length2, min_sup, min_conf, min_sup_num,
#                                  item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "KEY", support,
#                                  i + 1)
#         else:
#             min_sup_num = int(math.floor(data_length2 * min_sup))
#             saveRuleToMysql3(data_length2, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "KEY", 0.0, i + 1)
#
#         if len3 != 0:
#             for item in rule3:
#                 min_sup_num = int(math.floor(data_length3 * min_sup))
#                 support = calSupport(list(item[0]), list(item[1]), resValueSet)
#
#                 saveRuleToMysql3(data_length3, min_sup, min_conf, min_sup_num,
#                                  item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "VALUE", support,
#                                  i + 1)
#         else:
#             min_sup_num = int(math.floor(data_length3 * min_sup))
#             saveRuleToMysql3(data_length3, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "VALUE", 0.0, i + 1)
#
#         if len4 != 0:
#             for item in rule4:
#                 min_sup_num = int(math.floor(data_length4 * min_sup))
#                 support = calSupport(list(item[0]), list(item[1]), keyAndValue)
#
#                 saveRuleToMysql3(data_length4, min_sup, min_conf, min_sup_num,
#                                  item[2], ','.join(list(item[0])), ','.join(list(item[1])), name, no, "TAGINSIDE",
#                                  support, i + 1)
#         else:
#             min_sup_num = int(math.floor(data_length4 * min_sup))
#             saveRuleToMysql3(data_length4, min_sup, min_conf, min_sup_num, 0.0, "无", "无", name, no, "TAGINSIDE", 0.0,
#                              i + 1)