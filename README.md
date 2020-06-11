# FPGrowth

## introduce

1.fp_growth.py 
>fp_growth 算法实现

2.MySQLForFPGrowth.py
>连接数据库从中取得原始数据

3.main.py
>主函数，调用以上两个文件进行操作

4.fpTemplate.py
>主函数的模板程序，传入数据源及支持度置信度，生成结果txt
>
5.mainForKeyOrValue.py
>单独分析key或者value的关联度 （在node，way，relation中）
>
6.xlsxOperate.py
>读取xlsx分级文件，并生成某些有用数据
>

7.xlsxReadLevel3.py
>读取xlsx分级文件，生成分类挖掘的tag数量降序
>

8.classification.py
>生成分类挖掘的结果，存放到log/classRes路径，仔细看看注释，里面还有小bug


9.spare和test.py
>没啥用的，写论文的时候粘贴的代码在这里调一调格式
>

10.fixRelation.py
>sax解析后发现里面有null，找半天没发现错误，这里就写一个脚本修复那个relation表。
>就是sax解析结束后，跑一遍这个程序即可，建议还是修复sax为好。
>

## download
####以下数据出自北京市的分析结果 
#####其中osm_rule2是最终的规则。这里是按照支持度和置信度交叉跑的结果。

 | **内容** | **大小** | **链接** |
| :-----:| :----: | :----: |
| osm_node | 173MB | [点我下载](https://oss.sumtudou.cn/something/osm/osm_node.sql) |
| osm_road | 40MB | [点我下载](https://oss.sumtudou.cn/something/osm/osm_road.sql) |
| osm_relation | 1MB | [点我下载](https://oss.sumtudou.cn/something/osm/osm_relation.sql) |
| osm_tag | 40MB | [点我下载](https://oss.sumtudou.cn/something/osm/osm_tag.sql) |
| osm_rule2 | <1MB | [点我下载](http://sumtudou.oss-cn-shanghai.aliyuncs.com/something/osm/osm_rule2.sql) |
