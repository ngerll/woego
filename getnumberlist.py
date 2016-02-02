# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import json
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Cookie':'StaffLoginInfo=LILP60; cklflag=1; ckpcode=71; cksid=LILP60; BIGipServerWEG-WEBAPP2=1795499396.41030.0000; BIGipServerWEG-WEBAPP1=1694836100.25675.0000; CNZZDATA1257374541=828476400-1454298228-http%253A%252F%252Fwww.woego.cn%252F%7C1454298228; WOEGO_JSESSIONID=219D7832346C4B66964EBD75691A4D0D'}


def getboxlist(orderid,chnlid,chnlname,areacode):
    boxlist = []
    url = 'http://www.woego.cn/woego/order/toOrderDetails?orDerId=%s' % orderid
    respone = requests.get(url,headers=head)

    context = respone.content

    paytime = re.findall('支付时间：(.*?)</div>',context,re.S)[0].strip().replace('-','/')

    idinfo = re.findall('<!--直接在这里解析串-->(.*?)<!--物流信息-->',context,re.S) #订单信息list

    for i in range(len(idinfo)):
        orderinfo = idinfo[i]  #单个商品订单信息
        ordersoup = BeautifulSoup(orderinfo,'lxml')
        sorderid = re.findall('<td id="collerpro_(.*?)"',str(ordersoup),re.S)[0]
        paymoney = re.findall('<td>￥(.*?)</td>',str(ordersoup),re.S)[0] #商品单价
        productid = ordersoup.find_all('font',{'color':"#006699"})[0].string.split('|')[0] #产品编码
        productname = ordersoup.find_all('font',{'color':"#006699"})[0].string.split('|')[1] #产品名称
        boxid = re.findall('卡包编号: (.*?) <p>',str(ordersoup),re.S)[0]
        gdsid = re.findall('kkkk="(.*?)"',str(ordersoup),re.S)[0]
        boxinfo = orderid,productid,productname,boxid,gdsid,sorderid,paymoney,paytime,chnlid,chnlname,areacode
        boxlist.append(boxinfo)

    return boxlist


def getnumberlist(boxlist):
    url = 'http://www.woego.cn/woego/order/cardBoxList'
    for list in boxlist:
        orderid = list[0]
        productid = list[1]
        productname = list[2]
        boxid = list[3]
        gdsid = list[4]
        sorderid = list[5]
        paymoney = list[6]
        paytime = list[7]
        chnlid = list[8]
        chnlname = list[9]
        areacode = list[10]

        datas = {'gdsid':gdsid,
                'orderProvice':'71',
                'queryStuta':'40',
                'boxCode':boxid
                }
        resopne = requests.post(url,headers=head,data=datas)

        context = resopne.content

        numberjson = json.loads(context)

        with open('d:/order/'+orderid+'.txt','wb') as file:
            for i in range(len(numberjson['cboxList'])):
                packageNum = numberjson['cboxList'][i]['cboxInfo']['packageNum']
                cboxNumberList = numberjson['cboxList'][i]['cboxNumberList']
                for j in range(len(cboxNumberList)):
                    packageno = len(numberjson['cboxList'])*packageNum
                    serialnumber = cboxNumberList[j]['serialNumber']
                    list =  "insert into huqiao_order values  ('%s','%s','%s','%s','%s','%s','%s',to_date('%s','yyyy/mm/dd,hh24:mi:ss'),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (str(orderid),str(sorderid),str(productid),str(serialnumber),str(productid),str(paymoney),'50',str(paytime),str(chnlid),areacode,'0','','','900',str(orderid),productname,str(packageno),str(int(paymoney)*100),'5000',str(5000-int(paymoney)*100),'0') \
                            + "\n" + "commit;"
                    file.write(list + '\n')


if __name__ == '__main__':
    orderid = '7116020109822640'
    chnlid = 'YMZHL'
    chnlname = '孝南毛陈杨爱莲MINI'
    areacode = '0712'
    getnumberlist(getboxlist(orderid,chnlid,chnlname,areacode))

