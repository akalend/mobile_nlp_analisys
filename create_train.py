#! /home/akalend/anaconda3/bin/python

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


# sql = "select negative,rate from review"
sql = "select ttext from sentiment  limit 3500"

with cnn.cursor() as cursor:
    cursor.execute(sql)
    rows =cursor.fetchall()

 

for row in rows:
    txt = row[0]
    ltext = txt.split()
    ltext = [ (lambda token: token if token[0:4] != "http" and token[0:1] != "Q" else '' )(token) for token in ltext ]
    ltext = [ (lambda token: token if token[0:1] != "@" and token[0:1] != "#" and token[0:2] != "RT" else '')(token) for token in ltext ]
    txt = " ".join(ltext)

    print("0;%s;" % txt )



sql = "select review,rate from review"

with cnn.cursor() as cursor:
    cursor.execute(sql)
    rows =cursor.fetchall()

for row in rows:
    txt = row[0]
    txt = txt.replace(';', '.')
    txt = txt.replace("\n", ' ')
    print("1;%s;" % txt )

