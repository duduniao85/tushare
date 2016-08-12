#coding=utf-8
__author__ = 'xuyuming'
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决ORACLE插入中文乱码问题
from urllib import urlopen
import time
from bs4 import BeautifulSoup
from sqlalchemy import *
import util
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2  #引入ORACLE专用字符集
from sqlalchemy.sql import select
from sqlalchemy.sql import text #用于导入自定义文本SQL
from sqlalchemy.schema import *
import pandas as pd
import tushare as ts
import re
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import datetime

#开始取上次数据日期
textdata=urlopen('http://list.jiuxian.com/1-0-0-0-0-0-0-0-0-0-0-0.htm?area=25#v2').read()
print textdata
