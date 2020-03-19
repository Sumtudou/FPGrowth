# -*- coding:utf-8 -*-
# @Time: 2020/3/19 23:29
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: mainForKeyOrValue.py
# 用于单独分析key或者value内部的关联度。

from mysqlForFpGrowth import *
from FpTemplate import *


nodeKeySet,nodeValueSet = getKeyOrValue(1)
wayKeySet,wayValueSet = getKeyOrValue(2)
relationKeySet ,relationValueSet= getRelationKeyOrValue()

getFpGrowthRes(nodeKeySet,"nodeKey",0.03 ,0.7)
getFpGrowthRes(nodeValueSet,"nodeValue",0.03 ,0.7)

getFpGrowthRes(wayKeySet,"wayKey",0.03 ,0.7)
getFpGrowthRes(wayValueSet,"wayValue",0.03 ,0.7)

getFpGrowthRes(relationKeySet,"relationKey",0.03 ,0.7)
getFpGrowthRes(relationValueSet,"relationValue",0.03 ,0.7)

allKeySet = nodeKeySet + wayKeySet + relationKeySet
allValueSet = nodeValueSet + wayValueSet + relationValueSet

getFpGrowthRes(allKeySet,"allKey",0.03 ,0.7)
getFpGrowthRes(allValueSet,"allValue",0.03 ,0.7)