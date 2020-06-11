# -*- coding:utf-8 -*-
# @Time: 2020/5/17 19:51
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: fixRelation.py
# 修复relation中出现的null字符串

# 不要运行了这个文件
# import pymysql
#
# # 共用部分，链接数据库
# #########我是分割线线线###########
# USERNAME = "root"
# PASSWD = "123456"
# ADDR = "localhost"
# DATABASE = "osm"
# db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
# cursor = db.cursor()
#
#
# #########我是分割线线线###########
# # 更新
#
# def fixRelations():
#     selectSql = "select * from " + "osm_relation"
#     cursor.execute(selectSql)
#     results = cursor.fetchall()
#
#     res = []
#     for item in results:
#         listItem = list(item)  # 2,3
#         if listItem[2] != None:
#             listItem[2] = listItem[2].replace("null","")
#             listItem[3] = listItem[3].replace("null","")
#
#         res.append(listItem)
#         #print(listItem)
#     cursor.execute('truncate table osm_relation')  # 先截断表
#
#     for item in res:
#         saveSql = "insert into osm_relation (id,nid,tagkey,tagvalue,status)" \
#                   " values('{0}','{1}','{2}','{3}','{4}')".format(item[0], item[1], item[2], item[3], item[4])
#         # print(sql)
#         try:
#             cursor.execute(saveSql)
#             db.commit()
#         except:
#             db.rollback()
#
# if __name__ == '__main__':
#     fixRelations()
# def screenTag(beforeKey, beforeValue, afterKey, afterValue):
#     flag = "WILLBEKILL"
#     for i in range(len(beforeKey)):
#         fs = False
#         for j in range(len(afterKey)):  # 去掉分类的tag对
#             if beforeKey[i] == afterKey[j] and beforeValue[i] == afterValue[j] :
#                 beforeKey[i] = flag
#                 beforeValue[i] = flag
#                 fs = True
#                 break
#         if fs == False:           # 去掉黑名单的tag对
#             for iter in blackList:
#                 if iter in beforeKey[i]:
#                     beforeKey[i] = flag
#                     beforeValue[i] = flag
#                     break
#     #利用正则表达式去掉值为flag的字符串
#     keys = list(filter(lambda x: x != flag, beforeKey))
#     values = list(filter(lambda x: x != flag, beforeValue))
#     return keys, values
# #导入python操作mysql的包
# import pymysql
# #本地数据库的配置文件，包含账号密码端口等
# USERNAME = "root"
# PASSWD = "123456"
# ADDR = "localhost"
# DATABASE = "osm"
# db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
# cursor = db.cursor()
#
# #保存关联规则到数据库
# def saveRuleToMysql(data_len, min_sup, min_conf, min_sup_num,
#                     confidence, first, second, name, no, type,support):
#
#     saveSql = "insert into osm_rule (data_len,min_sup,min_conf,min_sup_num," \
#               "confidence,first,second,name,no,type,status,support) values" \
#               "('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}'," \
#               "'{10}','{11}')".format(data_len, min_sup, min_conf, min_sup_num,
#                confidence, first, second, name, no, type,1,support)
#     try:
#         cursor.execute(saveSql)
#         db.commit()
#     except:
#         db.rollback()

#
# for i in range(0, 25):
#     step = i * 0.01         #步长为0.01
#     min_sup = 0.25 - step   #最小支持度
#     min_conf = 0.95 - step  #最小置信度
#
#     rule = getFpGrowthRes(min_sup, min_conf)
#
#     if len(rule) > 10  or i == 24:
#         saveRuleToMysql(rule)
#         break
#
# for i in range(0, 5):  # 0 1 2 3 4
#     min_sup = i * 0.02 + 0.01
#     min_conf = 1 - 0.05 * (i + 2)
#     rule1 = getFpGrowthRes(kv, newName + 'KV', min_sup, min_conf)
#     rule2 = getFpGrowthRes(resKeySet, newName + 'KEY', min_sup, min_conf)
#     rule3 = getFpGrowthRes(resValueSet, newName + 'VALUE', min_sup, min_conf)
#     rule4 = getFpGrowthRes(keyAndValue, newName + 'Tag-Inside', min_sup, min_conf)
