#coding=utf-8
__author__ = 'xuyuming'
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#爬取链家网挂牌房源

def http_post_for_deals(offset):
    """
    http://soa.dooioo.com/api/v4/online/house/ershoufang/search
    :param params:查询参数集合
    :param access_token:访问授权ID
            numPerPage:每次查询的数量
            offset:查询的偏移量
    :return:
    """
    headers={'User-Agent':\
                 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',\
             'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',\
             'Accept-Encoding':r'gzip, deflate, sdch',\
             'Accept-Language':'zh-CN,zh;q=0.8',\
             'Cache-Control':'max-age=0',\
             'Connection':'keep-alive',\
             'Cookie':'T=34Q-pLN1Avj-pLNoToQ4GJW0Dt4HjrCsXGKS3F',\
             'Host':'soa.dooioo.com',\
             'HTTPS':'1'}
    url=r'http://soa.dooioo.com/api/v4/online/house/ershoufang/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=ershoufang&cityCode=sh&client=wap&limit_count=100&limit_offset='+str(offset)
    print url
    r=requests.get(url,headers=headers)
    return r.json()



if __name__ == '__main__':
    hasMoreData=1
    offset=72900
    while(True):
        time.sleep(2)
        jsonObj= http_post_for_deals(offset)
        hasMoreData=jsonObj.get('data').get('has_more_data')
        if hasMoreData == 0 :
            break
        itemList= jsonObj.get('data').get('list')
        filename=r'd:\temp\guapai20160804.csv'
        if len(itemList)>0:
            df=pd.DataFrame(itemList)
            try:
                del df['mainPhotoUrl']
            except:
                pass
            del df['tags']
            if os.path.exists(filename):
                df.to_csv(filename, mode='a', header=None,encoding='GBK')
            else:
                df.to_csv(filename,encoding='GBK')
        else:
            break
        offset+=100
