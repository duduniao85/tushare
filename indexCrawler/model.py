#encoding:utf8
'''
定义了需要加载的指数表模型
'''
__author__ = 'xuyuming'

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String,Float, MetaData, ForeignKey,DATE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

#from pyinotify import *

path = "/tmp"

#SQLAlchemy
engine = create_engine('mysql://fundbi:fundbi@localhost/fundbi?charset=utf8', echo=True)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class goldHistoricalData(Base):
    '''
    记录黄金历史行情的模型
    '''
    __tablename__ = 'goldHistoricalData'

    tradeday = Column(DATE, primary_key=True)
    closeprice = Column(Integer)
    openprice=Column(Integer)
    highprice=Column(Integer)
    lowprice=Column(Integer)
    tradevol=Column(String)
    chgpcnt=Column(Float)

    def __init__(self, tradeday,closeprice,openprice,highprice,lowprice,tradevol,chgpcnt):
        self.tradeday = tradeday
        self.closeprice = closeprice
        self.openprice=openprice
        self.highprice= highprice
        self.lowprice= lowprice
        self.tradevol= tradevol
        self.chgpcnt= chgpcnt

    def __repr__(self):
        return "<Metadata('%s','%s')>" % (self.tradeday,self.closeprice)

