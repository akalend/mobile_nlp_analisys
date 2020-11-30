#! /home/akalend/anaconda3/bin/python

# converter from Db to negative.csv 
import pymysql


loc_conf = {
        'mysql_user': 'client',
        'mysql_db': 'nlp',
        'mysql_host': '127.0.0.1',
        'mysql_password': 'client',
    }
    


try:
    cnn = pymysql.connect(host=loc_conf['mysql_host'],
                         user=loc_conf['mysql_user'],
                         password=loc_conf['mysql_password'],
                         db=loc_conf['mysql_db'],
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.SSCursor,     # DictCursor,
                         autocommit=True)
except:
    print ( '{"result" : "connection error"}')


sql = "select negative,rate from review"

with cnn.cursor() as cursor:
    cursor.execute(sql)
    rows =cursor.fetchall()


for row in rows:
    print("%d;%s" % (row[1], row[0]) )
