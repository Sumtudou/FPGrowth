# -*- coding:utf-8 -*-
# @Time: 2020/5/17 19:51
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: fixRelation.py
# 修复relation中出现的null字符串

#不要运行了这个文件
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
