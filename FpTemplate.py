# -*- coding:utf-8 -*-
# @Time: 2020/3/20 00:32
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: FpTemplate.py
# 写到分析node的key时想到，每次都重写一次main多麻烦
# 因而写一个模板函数放在这里调用即可。
# 调用此函数，传入数据源及其他参数即可直接生成结果。

# Param :data :数据源； fileName:保存的文件名；
#       min_support：最小支持度，用小数表示（小于1）
#       min_conf:    最小置信度
#返回值：len，长度
#rule_list：规则列表，这个直接传回去好保存
#length : data_length
from fp_growth import *
import math


def getFpGrowthRes(data, fileName, min_support, min_conf):
    current_path = os.getcwd()
    if not os.path.exists(current_path + "/log"):
        os.mkdir("log")
    save_path = current_path + "/log/" + fileName + '.txt'

    length = len(data)
    print("***********", fileName, "***********")
    print("数据的组数", length)

    min_support_num = int(math.floor(length * min_support))  # 最小支持度对应的出现次数,次数算上这个数。向下取整
    print("min_support_num=", min_support_num, "次")
    print("min_conf=", min_conf * 100, "%")
    print("min_support=", min_support * 100, "%")

    start = time.perf_counter()
    fp = Fp_growth()
    rule_list = fp.generate_R(data, min_support_num, min_conf)
    end = time.perf_counter()
    print("\nfpGrowth's Runtime is:", round(end - start + 0.001, 2), "second\n")

    save_rule(rule_list, save_path, length, min_support_num,min_support,min_conf)
    print("***********我是下分割线***********\n\n")
    return len(rule_list) , rule_list ,length

