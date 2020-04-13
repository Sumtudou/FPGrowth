# -*- coding:utf-8 -*-
# @Time: 2020/4/5 16:57
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: relationKey.py

from mysqlForFpGrowth import *
from FpTemplate import *

relationKeySet,relationValueSet= getRelationKeyOrValue()

delKey = ["route","type"]

# for item in relationKeySet:
#     for delKeyItem in delKey:
#         if delKeyItem in item:
#             relationKeySet.remove(item)
#             break

for ggg in relationKeySet:
    print(ggg)

print("**************************")


newKeySet = []
for item in relationKeySet:
    if "route" not in item and "type" not in item:
        newKeySet.append(item)

for i in newKeySet:
    print(i)
getFpGrowthRes(newKeySet,"relationKey",0.08 ,0.8)  #这个是relation的key，因为项集有点多，提高一下条件

