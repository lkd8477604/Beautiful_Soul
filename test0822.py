#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests, time
import json
import pymongo

def get_url():
    urls_list = []
    urls = 'https://www.douyu.com/directory'
    data = requests.get(urls)
    Soup = BeautifulSoup(data.text, 'lxml')
    list = Soup.select('.r-cont.column-cont  dl  dd  ul  li  a')
    for i in list:
        urls = i.get('href')
        # print (urls)
        urls_list.append(urls)
    print (urls_list)
    return urls_list

def get_rank(urls_list):
    list_data = []
    summary_data = []
    # url = 'https://www.douyu.com/g_DOTA2'

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        "Cookie": 'dy_did=b1223239a766473f9f51c17561051501; acf_recruitMsgNum63412784=9; acf_auth=f9d2fynlBirTIQazpFhkuw9ReGJL3%2Fj%2BEde0phtjYMjI6Eaktl%2BtHJBg2D0diAayfTpcQVTEcIK2DBJeth4PLfNKwX7W7eLF9FkPPDnFmD1BgqqoqPRp; wan_auth37wan=10548e70975czgxKC27Fdsb0kJHg%2Fw3V6VLq60XcP5afazagVqqcoJlTTRnTsA2cfLuDof%2Bo5F8l0ncsdGcxxON9LhLO0RtjrWjlFILbN3KA5LjMyQ; acf_uid=63412784; acf_username=63412784; acf_nickname=%E6%98%A5%E8%BF%9F%E8%BF%9F%E7%87%95%E5%AD%90%E5%A4%A9%E6%B6%AF; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_ct=0; acf_ltkid=79690937; acf_biz=1; acf_stk=8707494e206cfb24; PHPSESSID=41kqvulrmjcqbdq5aar8bhc1e1; _dys_lastPageCode=page_studio_normal,; acf_ccn=8ca185259b2e162de154e485c36dc0d5; acf_did=b1223239a766473f9f51c17561051501; smidV2=20180620191947a1a5e013a5248ecc4adfaaf18ab4a54100c278613c062b020; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1534594655,1534785149,1534861316,1534939025; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1534961151'
    }
    for url_end in urls_list:
        url = 'https://www.douyu.com' + url_end
        print ('Now start open {}'.format(url))
        get_data = requests.get(url, headers=headers)
        Soup = BeautifulSoup(get_data.text, 'lxml')
        names = Soup.select('.ellipsis.fl')
        nums = Soup.select('.dy-num.fr')
        titles = Soup.select('.mes h3')
        hrefs = Soup.select('#live-list-contentbox  li  a')

        # print (desc)
        for name, num, href, title in zip(names, nums, hrefs, titles):
            data = {
                '主播': name.get_text(),
                '标题': title.get_text().split('\n')[-1].strip(),
                '链接': 'https://www.douyu.com' + href.get('href'),
                '人气指数': float(num.get_text()[:-1]) if '万'in num.get_text() else float(num.get_text())/10000,
            }
            # print (data)
            list_data.append(data)
        time.sleep(1)
    for i in list_data:
        if i['人气指数'] > 30:
            summary_data.append(i)
            print (i)
    return summary_data
    # with open('D:\douyu_host.txt', 'w') as w_data:
    #     w_data.writelines(json.dumps(summary_data))

def open_data():
    with open('D:\douyu_host.txt', 'r') as r_data:
        r_data = json.load(r_data)
        for i in r_data:
            print (i)
        return r_data
def w_to_db(r_data):
    client = pymongo.MongoClient('localhost', 27017)
    walden = client['walden']
    sheet_tab = walden['sheet_tab']
    for data in r_data:
        sheet_tab.insert_one(data)

def check_from_db():
    client = pymongo.MongoClient('localhost', 27017)
    walden = client['walden']
    sheet_tab = walden['sheet_tab']
    for data in sheet_tab.find({'人气指数':{'$lte':40}}):
        print (data)
urls_list = get_url()
r_data = get_rank(urls_list)

# open_data()
# w_to_db(r_data)
# check_from_db()
