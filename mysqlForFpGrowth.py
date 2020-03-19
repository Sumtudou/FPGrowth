import pymysql

# 共用部分，链接数据库
#########我是分割线线线###########
USERNAME = "root"
PASSWD = "123456"
ADDR = "localhost"
DATABASE = "osm"
db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)
cursor = db.cursor()


#########我是分割线线线###########

# 获取tag和value分析频繁二项集
def getDataFromMysql(tableName):
    selectSql = "select * from " + tableName
    cursor.execute(selectSql)
    results = cursor.fetchall()
    res = []
    for item in results:
        resItem = []
        resItem.append(item[1])
        resItem.append(item[2])
        res.append(resItem)
    # print(res)
    return res


### 执行select语句，将返回的数据存入level1表中
###sql：传入的select 语句

def saveLevel1(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    cursor.execute('truncate table osm_tag_level1')  # 先截断表

    for item in results:
        saveSql = "insert into osm_tag_level1 (id,tagkey,tagvalue,father,fid,status)" \
                  " values('{0}','{1}','{2}','{3}','{4}','{5}')".format(item[0], item[1], item[2], item[3], item[4],
                                                                        item[5])
        # print(sql)
        try:
            cursor.execute(saveSql)
            db.commit()
        except:
            db.rollback()
    return 1


# 单独获取node、的key及value并转好成数据
def getNodeKeyOrValue():
    sql = "SELECT * FROM osm_node WHERE tagkey IS NOT NULL;"
    cursor.execute(sql)
    results = cursor.fetchall()
    keySet = []
    valueSet = []

    for item in results:
        # print(item[10],item[11])
        keys = item[10].split(';')
        keys.pop()
        keySet.append(keys)

        values = item[11].split(';')
        values.pop()
        valueSet.append(values)

    # print(keySet,'\n',valueSet)
    return keySet, valueSet


# 单独获取node的key及value并转好成数据
# 单独获取way的key及value并转好成数据
def getKeyOrValue(flag):
    NodeSql = "SELECT tagkey, tagvalue FROM osm_node WHERE tagkey IS NOT NULL;"
    WaySql = "SELECT tagkey, tagvalue FROM osm_road WHERE tagkey IS NOT NULL;"
    if flag == 1:
        cursor.execute(NodeSql)
    else:
        cursor.execute(WaySql)

    results = cursor.fetchall()
    keySet = []
    valueSet = []

    for item in results:
        # print(item[10],item[11])
        keys = item[0].split(';')
        keys.pop()
        keySet.append(keys)

        values = item[1].split(';')
        values.pop()
        valueSet.append(values)

    return keySet, valueSet


def getRelationKeyOrValue():
    cursor.execute("SELECT tagkey ,tagvalue,fid FROM osm_tag WHERE father = 'relation';")
    results = cursor.fetchall()

    keySet = []
    valueSet = []
    keys = []
    values = []
    tempId = 0
    isFirst = True

    for item in results:
        if isFirst:
            tempId = int(item[2])
            keys.append(item[0])
            values.append(item[1])
            isFirst = False
            continue

        if int(item[2]) == tempId:
            keys.append(item[0])
            values.append(item[1])
        else:
            keySet.append(keys)
            valueSet.append(values)

            keys = []
            keys.append(item[0])
            values = []
            values.append(item[1])

            tempId = int(item[2])

    return keySet, valueSet

