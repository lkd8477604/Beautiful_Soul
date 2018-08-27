#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup

list_data = []
with open('F:\douyu.html', encoding='utf-8') as data:
    soup = BeautifulSoup(data, 'lxml')
    leimus = soup.select('#live-list-contentbox > li > a > p')
    for leimu in leimus:
        dict_data = {
            'leimu':leimu.get_text()
        }
        # print (dict_data)
        list_data.append(dict_data)
print (list_data)
for index,rank in enumerate(list_data):
    if rank['leimu'].upper() == 'DOTA2':
        print ('Today DOTA2 rank at {} positon'.format(index+1))