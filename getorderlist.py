# -*- coding: utf-8 -*-
import requests
import json

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Cookie': 'StaffLoginInfo=LILP60; cklflag=1; ckpcode=71; cksid=LILP60; BIGipServerWEG-WEBAPP2=1795499396.41030.0000; BIGipServerWEG-WEBAPP1=1694836100.25675.0000; CNZZDATA1257374541=828476400-1454298228-http%253A%252F%252Fwww.woego.cn%252F%7C1454298228; WOEGO_JSESSIONID=219D7832346C4B66964EBD75691A4D0D'}

def getorderinfo(beginDate,endDate):
    datas = {'beginDate':beginDate,
             'endDate':endDate,
             'productType':'100',
             'payFlag':'1',
             'timeType':'1',
             # 'shopProvinceCode':'11',
             'Etype':'1'
    }

    url = 'http://www.woego.cn/woego/orderquery/exportsellList'
    respone = requests.get(url,headers=head,params=datas)

    context = respone.content

    with open('d:/1.xls','wb') as file:
        file.write(context)

if __name__ == '__main__':
    beginDate = '2016-01-29'
    endDate = '2016-01-31'
    getorderinfo(beginDate,endDate)