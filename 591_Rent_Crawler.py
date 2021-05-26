
# coding: utf-8
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pymongo import MongoClient

# Mongodb Client
def mongo_base(host,port,database,table,data):
    client = MongoClient(host, port)
    db=client[database]
    rent = db[table]
    rent.insert_many(json.loads(data.T.to_json()).values())


# In[88]:


# get total_count
cookies = "webp=1; PHPSESSID=gdjh67ehetup773aha4rqtsh23; T591_TOKEN=gdjh67ehetup773aha4rqtsh23; _ga=GA1.3.2075565203.1621857871; _gid=GA1.3.726406820.1621857871; _ga=GA1.4.2075565203.1621857871; _gid=GA1.4.726406820.1621857871; tw591__privacy_agree=0; _fbp=fb.2.1621857872952.1207424375; new_rent_list_kind_test=0; user_index_role=1; __auc=d207d3651799e5ea7167b05ec29; localTime=2; imgClick=10837387; __utmc=82835026; __utmz=82835026.1621865620.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); is_new_index=1; is_new_index_redirect=1; __utma=82835026.2075565203.1621857871.1621868451.1621918305.3; DETAIL[1][10918147]=1; DETAIL[1][10893408]=1; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A8%3A%2210893408%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A8%3A%2210918147%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A8%3A%2210937793%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A8%3A%2210710567%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A8%3A%2210836244%22%3B%7D%7D; __asc=47690f70179a93206964c3984c6; _gat_UA-97423186-1=1; _gat=1; _gat_testUA=1; _gat_rentDetail=1; _gat_rentNew=1; _dc_gtm_UA-97423186-1=1; XSRF-TOKEN=eyJpdiI6ImRzT1dyRDQ0VFkzZVVqWkpJaTN2Y0E9PSIsInZhbHVlIjoiT0hcL0RcL21ab0w2SXFzZHFJT2dxN2hHV1VBTjdvcWNwdHdJdW95NmZMemZteVpuZU5xb1BaNGRZXC9GMkdIcTdLQ0NSYTJLM0kzWkxycyt6Qnd1eGNHdkE9PSIsIm1hYyI6ImMzNDMxZTUwODE3YjExOGQ0ZDY3NGM2MjcyMDk2YTUxYjNkZThjYmEzNGVkYzY3YmI0NjE5NzgwNDFjNDgwMGEifQ%3D%3D; 591_new_session=eyJpdiI6InFvRVpJUkpmMVNXXC80VnhiV1M1bGVRPT0iLCJ2YWx1ZSI6Ims2VThcL2pkejlYUHBvRzV5Z2VFakhRQkRpSVJXQ3VSaFpVeVF3cUE1Q1wvb2pcL0JwYXNxS3FwNVdjdzBIMnhZeTg5Q1h2YlU3YXkrMGsrREdFMHYzc29nPT0iLCJtYWMiOiI2NDQxZmIwNzJlMDRmNzZjNGM2MWY5MDY2OTA0OTQwOTE0YTQ2NDI3YzFmNDY5NzQ2ZDJhZThhMTlhMjRhYmIxIn0%3D; urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82"
csrf_token = "NEvIxy4Z9E5x7gJ0kl3UI78RU124iVWYlW61TubM"
response = requests.get('https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=0', 
                  headers={"X-CSRF-TOKEN":csrf_token,"Cookie":cookies})
total_count = response.json()['records'].replace(',', '')



linkmans =[]#出租者
nick_names = []#身分
type_names =[]#型態
phone_numbers = []#電話
kind_names = []#現況
genders =[]#性別要求
url_ids=[]
region_names =[]



def parse_rent_object(post_id):
    response = requests.get("https://rent.591.com.tw/rent-detail-"+str(post_id)+".html")
    soup = BeautifulSoup(response.text, "html.parser")
    
    phone_number = ''
    type_name = ''
    gender = 2
    try:
        # get Phone Number
        phone_number = soup.find("span", {"class": "dialPhoneNum"})['data-value']
        if phone_number == '':
            phone_number = soup.find("div", {"class": "hidtel"}).getText().strip()
            phone_number = phone_number.replace('-', '')
    except:
        pass
    try:
        # get 型態
        elements = soup.find("div", {"class": "detailInfo clearfix"}).find("ul", {"class": "attr"}).find_all('li')
        for element in elements:
            if element.getText().strip()[0:2] == '型態':
                type_name = element.getText().strip().split(":")[1].strip()
                break
    except:
        pass
    try:
        # gender 性別要求
        gender_dict = {"女生":0,"男生":1,"男女生皆可":2}
        gender = "男女生皆可"
        elements = soup.find("ul", {"class": "clearfix labelList labelList-1"}).find_all('li', {"class": "clearfix"})
        for element in elements:
            if element.find("div", {"class": "one"}).getText().strip() == '性別要求':
                gender = element.find("div", {"class": "two"}).find("em").getText().strip()
                break
    except:
        pass
    phone_numbers.append(phone_number)
    genders.append(gender_dict[gender]) 
    type_names.append(type_name) 
    



# response.json()['data']['data']
# print(int(total_count))
for x in range(0, int(total_count), 30):
    url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=0&firstRow='+str(x)
    response = requests.get(url, 
                  headers={"X-CSRF-TOKEN":csrf_token,"Cookie":cookies})
    data = response.json()['data']['data']
    for i in range(30):
        linkmans.append(data[i]['linkman'])
        nick_names.append(data[i]['nick_name'].split(" ")[0])
        kind_names.append(data[i]['kind_name'])
        url_ids.append(data[i]['post_id'])
        region_names.append(data[i]['region_name'])
        parse_rent_object(data[i]['post_id'])


# In[92]:


data = pd.concat([pd.DataFrame({'linkman': linkmans}), pd.DataFrame({'nick_name':nick_names}), pd.DataFrame({'type_name':type_names}), 
         pd.DataFrame({'kind_name':kind_names}), pd.DataFrame({'phone_number':phone_numbers}), pd.DataFrame({'gender':genders}), pd.DataFrame({'url_id':url_ids}), pd.DataFrame({'region_name':region_names})], axis=1)


mongo_base("localhost",27017,"591","rent",data)

