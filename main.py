from mysqlForFpGrowth import *
from fp_growth import *
import math

data = getDataFromMysql()

current_path = os.getcwd()
if not os.path.exists(current_path + "/log"):
    os.mkdir("log")
save_path = current_path + "/log/fpgrowth.txt"

len = len(data)
print("数据的组数",len)
min_support = 0.0100  # 最小支持度,小数。
min_conf = 0.5       # 最小置信度,小数。

min_support_num = int(math.floor(len * min_support)) #最小支持度对应的出现次数,次数算上这个数。向下取整
print("min_support_num=",min_support_num,"次")
print("min_conf=",min_conf*100,"%")
print("min_support=",min_support*100,"%")

start = time.perf_counter()
fp = Fp_growth()
rule_list = fp.generate_R(data, min_support_num, min_conf)
end = time.perf_counter()
print("\nfpGrowth's Runtime is:",round(end - start + 0.001, 2), "second\n")

save_rule(rule_list, save_path)
