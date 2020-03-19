from FpTemplate import *
from mysqlForFpGrowth import *


data = getDataFromMysql("osm_tag_level1")
fileName = "fpgrowth"
min_support = 0.0100  # 最小支持度,小数。
min_conf = 0.8       # 最小置信度,小数。
getFpGrowthRes(data,fileName,min_support,min_conf)
