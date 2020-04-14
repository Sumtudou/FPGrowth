# -*- coding:utf-8 -*-
# @Time: 2020/3/26 11:42
# @Author: sumtudou
# @Email: sumtudou98@gmail.com
# @File: levelRead.py

from FpTemplate import *
def layer_rules_object(object_tag, layer_rule):
    for index, rule in layer_rule.iterrows():
        #        print(rule)
        #        print(rule['osm_tags'])
        #        print(object_tag)
        if '!!' in rule['osm_tags']:  # use !! replace ||
            r = rule['osm_tags'].split('!!')
            # print("r:",r)
            for rule_tag in r:
                if rule_tag.strip() in object_tag:
                    return rule['l3code'], rule['l2layer']
        elif '&&' in rule['osm_tags']:
            r = rule['osm_tags'].split('&&')
            flag = 1
            for rule_tag in r:
                if object_tag.find(rule_tag.strip()) == -1:  # s.find("is") == -1
                    flag = 0
                    break
            if flag == 1:
                return rule['l3code'], rule['l2layer']
        elif rule['osm_tags'].strip() in object_tag:
            return rule['l3code'], rule['l2layer']
    return 9999, 'unknown'

if __name__ == '__main__':
    data = [["e1","1"],["e2","2"],["e3","3"]]
    getFpGrowthRes(data,"ggg",0.80, 0.01)
