#! /home/akalend/anaconda3/bin/python
import pymysql, time
import pandas as pd
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
                         cursorclass=pymysql.cursors.DictCursor,
                         autocommit=True)
except:
    print ( '{"result" : "connection error"}')
    exit()


sql = "SELECT negative FROM review"
# sql = "SELECT 1"
try:
    with cnn.cursor() as cursor:
        cursor.execute(sql)
        rows =cursor.fetchall()

except Exception as err:
    print(err)
    print('------ SQL 1 error ---- ' )
    exit()

# print(rows)
negative = pd.DataFrame(rows)
r = negative.head(100)
# print(r)

from gensim.models import Word2Vec

w2v_model = Word2Vec(
    min_count=10,
    window=2,
    size=300,
    negative=10,
    alpha=0.03,
    min_alpha=0.0007,
    sample=6e-5,
    sg=1)

w2v_model.build_vocab(data)
