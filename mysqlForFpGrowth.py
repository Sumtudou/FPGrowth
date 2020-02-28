import pymysql

def getDataFromMysql():
        USERNAME = "root"
        PASSWD = "123456"
        ADDR = "localhost"
        DATABASE = "osm"
        TABLE = "user"
        db = pymysql.connect(ADDR, USERNAME, PASSWD, DATABASE)

        cursor = db.cursor()
        cursor.execute("select * from osm_tag")
        results = cursor.fetchall()

        res = []
        for item in results:
            resItem = []
            resItem.append(item[1])
            resItem.append(item[2])
            res.append(resItem)
        #print(res)
        return res



