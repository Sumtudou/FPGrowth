import os
import xlrd
import xlwt
import mysqlForFpGrowth


#根据level1表的分级，目前没有什么用处。
def readXlsx():
    current_path = os.getcwd()
    path = current_path + '/file/level1-3 revised by zhao.xlsx'
    #print(path)
    readbook = xlrd.open_workbook(path)

    worksheet = readbook.sheet_by_name("level1")
    # print(worksheet)
    nrows = worksheet.nrows  # 获取该表总行数
    ncols = worksheet.ncols  # 获取该表总列数
    res = []
    for i in range(1, nrows - 1):  # 去掉首行的表头和结尾的unsure
        # print(worksheet.row_values(i))  # 以列表形式读出，列表中的每一项是str类型
        item = worksheet.row_values(i)
        if item[4] == "Point":
            res.append([item[1], "node"])
        elif item[4] == "Line":
            res.append([item[1], "way"])
        elif item[4] == "Polygon":
            res.append([item[1], "relation"])
    theSql = "select * from osm_tag where "
    first =  True
    for item in res:
        str1 = "(tagkey = '"+item[0] + "' and father = '"+item[1]+"')"
        if(first):
            theSql = theSql + str1
            first = False
        else:
            theSql = theSql + "OR" + str1
    #print(theSql)
    return theSql

# if __name__ == '__main__':
#     sql = readXlsx()
#     #print("ggg"+sql)
#     mysqlForFpGrowth.saveLevel1(sql)