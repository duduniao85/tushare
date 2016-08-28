#coding=utf-8
'''
2014_global_ips.txt文件是2014年的ip地址库，记录的是每个IP地址段对应的运营商，格式为：
开始地址   结束地址  国家  运营商

1）请把这个地址库用 SQL方式插入到Mysql数据库表中（表结构自行定义）
2）自定义两个ip地址，判断该地址所属国家和运营商。
'''
__author__ = 'xuyuming'
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决ORACLE插入中文乱码问题
import time
from sqlalchemy import *
from sqlalchemy.schema import *
import pandas as pd
import re
import pymongo
import json
def getTxtData(filename):
    '''
    读取2014_global_ips.txt文件
    :param filename:文件路径和地址
    :return:数据集 dataframe类型
    '''
    #读取TXT文件
    file_object = open(filename)
    list_of_all_the_lines = file_object.readlines( )
    count=0
    ipList=[];
    for line in list_of_all_the_lines:
        if line:
            list= (re.sub(r'[\s]+', ' ', line)).strip().split(' ')
            if len(list)>1:
                item={
                    'begin_ip':list[0],
                    'numStartIp':toInt(list[0]),
                    'end_ip':list[1],
                    'numEndIp':toInt(list[1]),
                    'country':list[2],
                    'region':list[3] if len(list)>3 else ''
                }
                ipList.append(item)
    return pd.DataFrame(ipList)
def save2MongoDB(data):
    '''
    将DATAFRAME数据存入到MONGODB当中，利用Dataframe的API完成快速操作
    :param data:
    :return:
    '''
    conn = pymongo.MongoClient('localhost',27017)
    #先清空表数据
    conn.db.globalIpData.remove()
    conn.db.globalIpData.insert(json.loads(data.to_json(orient='records')))
def save2DB(data):
    '''
    将DATAFRAME类型的数据落地到数据库当
    :param dbUesrname: mysql数据库用户名
    :param dbUserpwd: mysql密码
    :param dbName: mysql数据库
    :return:无返回
    '''
    db_engine=create_engine('mysql://fundbi:fundbi@localhost/fundbi?charset=utf8', echo=True)
    conn=db_engine.connect()
    data.to_sql('ip_region_mapp',db_engine,if_exists='replace',index=False)
    conn.close()
def toInt( givenIp):
    '''
    将字符串型的IP转成整数
    :param givenIp: 需要转成整数的IP
    :return:整型IP
    '''
    return int(givenIp.split('.')[0])*1000000000+int(givenIp.split('.')[1])*1000000+int(givenIp.split('.')[2])*1000+int(givenIp.split('.')[3])


def getRegion(ipAddress):
    '''
    根据自定义ip地址，判断该地址所属国家和运营商。
    :param ipAddress:
    :return: a dict {'country':countryname,'region':regionname}
    '''
    db_engine=create_engine('mysql://fundbi:fundbi@localhost/fundbi?charset=utf8', echo=True)
    conn=db_engine.connect()
    meta=MetaData()
    t = Table("ip_region_mapp",meta, autoload=True, autoload_with=db_engine)#连接指定的表名
    numIpAddress=toInt(ipAddress)
    s=select([t]).where(and_(t.c.numStartIp<=numIpAddress,t.c.numEndIp>=numIpAddress))#查找是否该交易日已经有了对应的数据
    result=conn.execute(s).fetchall() #取得所有结果集合LIST
    for i in result:
        print i[1],i[5]#,i[4],i[3]
    conn.close()
def getRegionByMongo(ipAddress):
    '''
    从MONGODB数据库表当中获取当前IP所属的地区
    :param ipAddress:
    :return:
    '''
    numIpAddress=toInt(ipAddress)
    conn = pymongo.MongoClient('localhost',27017)
    db=conn.db
    print numIpAddress
    count=db.globalIpData.find().count()
    result=db.globalIpData.find_one({'numStartIp':{'$lte':numIpAddress},'numEndIp':{'$gte':numIpAddress}})
    print result['country'],result['region']

#save2DB(getTxtData(r'D:\temp\2014_global_ips.txt'))
save2MongoDB(getTxtData(r'D:\temp\2014_global_ips.txt'))
getRegionByMongo('1.0.1.1')

#result:
#福建省 电信