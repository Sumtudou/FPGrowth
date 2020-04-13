from FpTemplate import *
from mysqlForFpGrowth import *

data = getDataFromMysql("osm_tag_level3")

#print(data)
fileName = "fpgrowth"
min_support = 0.00100  # 最小支持度,小数。
min_conf = 0.5        # 最小置信度,小数。
getFpGrowthRes(data,fileName,min_support,min_conf)
