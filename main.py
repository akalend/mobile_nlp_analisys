#! /home/akalend/anaconda3/bin/python
# from urllib.request import Request
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth

# html = urlopen("http://www.pythonscraping.com/pages/page1.html")
import requests
import pymysql, time

def parse_view(url):

    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"

    headers={
        'User-Agent': user_agent,
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }

    cookies={'ROBINBOBIN': "sf5rsthcbc5nl9sliqm2q35cv6",
             "guid":"d280dd3d41b378c7103f2297051b621b",
             "gha":"1",
             "yec":"1",
             "ssid":"1763759316"}

    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        webpage = response.text
        print( 'return:', response.status_code)
    except Exception as e:
        print(e)
        exit()

    if True:
        bsObj = BeautifulSoup( webpage );
        
        if bsObj is None:
            print('HTML is null')
            exit()
    #     review-list-2 review-list-chunk
        # return True
        review = bsObj.find("div", {"itemprop":"description"})
        return review.text


def parse_page(url, cnn, model, with_page):
    print(url)
    # return False

    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"

    headers={
        'User-Agent': user_agent,
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }


    proxies = {'http': '207.164.21.34:3128'}
    auth = HTTPProxyAuth('my_login', 'my_password')
    # proxies=proxies, auth=auth)


    cookies={'ROBINBOBIN': "sf5rsthcbc5nl9sliqm2q35cv6",
             "guid":"d280dd3d41b378c7103f2297051b621b",
             "gha":"1",
             "yec":"1",
             "ssid":"1763759316"}


    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        webpage = response.text
        if response.status_code != 200:
            print( 'return:', response.status_code)
            return False
    except Exception as e:
        print(e)
        exit()
        if e.code != 200:
            return 0
        #возвратить null, прервать или выполнять операции по "Плану Б"
    else:
        bsObj = BeautifulSoup(webpage);
        
        if bsObj is None:
            print('HTML is null')
            exit()
    #     review-list-2 review-list-chunk
        # return True
        review = bsObj.find_all("div", {"itemprop":"review"})
        i = 0
        for item in review:
            i +=1
            if i < with_page:
                continue
                    
            print('------------- reviw -----------', i)
            title = item.h3.get_text()
            print(title) 
            url_review = item.meta['content']
            text = parse_view(url_review)
            time.sleep(4)

            rait_ob = item.find("div", {"class": "product-rating tooltip-right"}) 
            rait = rait_ob['title']
            rate = rait.split(':')[1]

            # print(rate)
            plus = item.find("div", {"class": "review-plus"})
            plus =  plus.get_text()

            minus = item.find("div", {"class": "review-minus"})
            minus = minus.get_text()

            # +----------+--------------+------+-----+---------+----------------+
            # | Field    | Type         | Null | Key | Default | Extra          |
            # +----------+--------------+------+-----+---------+----------------+
            # | id       | int(11)      | NO   | PRI | NULL    | auto_increment |
            # | model    | varchar(30)  | YES  |     | NULL    |                |
            # | url      | varchar(45)  | YES  |     | NULL    |                |
            # | rate     | int(11)      | YES  |     | NULL    |                |
            # | positive | varchar(510) | YES  |     | NULL    |                |
            # | negative | varchar(510) | YES  |     | NULL    |                |
            # | review   | text         | YES  |     | NULL    |                |
            # | created  | int(10) unsigned | YES    | NULL 
            # +----------+--------------+------+-----+---------+----------------+

            sql = "INSERT INTO review(model,url,rate,positive,negative,review,title,created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                with cnn.cursor() as cursor:
                    cursor.execute(sql, (model,url_review,rate,plus,minus,text,title,int(time.time())))

            except Exception as err:
                print(err)
                print('------ SQL error: INSERT to nlp ---- ' )

        print('Ok')
        return i
#  подсчет рейтинга str(x[27:])



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


# цикл по страницам
base_url = "https://otzovik.com/reviews/"
# model_url = "smartphone_huawei_honor_x10_max/"
# model_url = "ayfon_7/"
# model_url = "apple_iphone_12_novinka_2020/"
# model_url = "smartphone_apple_iphone_11/"
# model_url = "smartphone_iphone_se_2020/"
# model_url = "smartphone_huawei_y5p/"
# model_url = "smartphone_huawei_p30/"
# model_url = "smartphone_samsung_galaxy_a01/"
# model_url = "smartphone_samsung_galaxy_m31s/"
# model_url = "smartphone_samsung_galaxy_s20_plus/"
# model_url = "smartphone_xiaomi_redme_1s/"
# model_url = "smartphone_xiaomi_redmi_go/"
# model_url = "smartphone_apple_iphone_8/"
# model_url = "smartphone_explay_pulsar/"
# model_url = "smartphone_explay_hd_quad/"
# model_url = "smartphone_huawei_mate_20_pro/"
# model_url = "sony_ericsson_xperia_x10_smartphone/"
# model_url = "smartphone_razer/"
# model_url = "smartphone_google_pixel_4/"
model_url = "/sotoviy_telefon_nokia_n9/"
model_url = "/smartphone_fly_fs458_stratus_7/"
# model_url = "smartphone_honor_20/"
# model_url = "smartphone_huawei_p40_pro_plus/"
# model_url = "smartphone_huawei_honor_v30/"
# model_url = "smartphone_honor_9x_pro/"
# model_url = "smartphone_huawei_honor_9/"
# model_url = "smartphone_huawei_honor_8a_prime/"
model = 'Fly FS458 stratus 7'
page=1
with_pos = 0
while(1):
    if page :
        url = base_url + model_url + str(page)
    else:
        url = base_url + model_url

    print('='*20)
    if 0 == parse_page(url, cnn, model, with_pos):
        break;
    with_pos = 0
    page += 1
    time.sleep(1)



