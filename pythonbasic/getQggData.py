#coding=utf-8
__author__ = 'xuyuming'
'''
    上线包包括 一个schema.ini文件，一个源文件
'''
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决ORACLE插入中文乱码问题
import time
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.orm import sessionmaker,mapper
from ftplib import FTP

def add_signal(filedate):
    '''
    用于读取钱滚滚文件接口数据
    :param filedate: 文件夹带的日期，即工作日日期，告知数据中心可以抽取具体的数据文件
    :return: 无返回
    '''
    db_engine = create_engine('oracle://xedm_trd:xpar@172.16.11.182:1821/xedm', echo=True)
    meta = MetaData()
    # 这句话就提供了一个表名，其他的，sqlalchemy都帮你做完了
    t = Table("TIMP_DATASOURCE_NOTIFY", meta, autoload=True, autoload_with=db_engine)

    class TIMP_DATASOURCE_NOTIFY(object):
        pass

    usermapper = mapper(TIMP_DATASOURCE_NOTIFY, t)
    DBSession = sessionmaker(bind=db_engine)
    session = DBSession()
    #  查询 -----------------
    query = session.query(TIMP_DATASOURCE_NOTIFY)
    rows=query.filter('beg_date='+"'"+filedate+"'").first()
    # 如果已经插入，重跑任务时，则重新插入信号
    if rows:
        session.delete(rows)
    record = TIMP_DATASOURCE_NOTIFY()
    record.s_type = 3
    record.s_code = 'FROM_QIANGUNGUN'
    record.beg_date = filedate  # 文件日期
    record.end_date = filedate  # 文件日期
    record.s_valid = '0'
    record.s_status = '0'
    record.create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    record.IMP_TYPE = '0'
    record.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    record.s_signal = '001007007'
    record.imp_date = time.strftime('%Y-%m-%d')
    record.pipe_id = '1'
    session.add(record)
    session.commit()
    session.close()

def get_load_date():
    '''
    取当前需要判断钱滚滚文件的数据日期
    :return: 数据日期
    '''
    db_engine = create_engine('oracle://xedm_trd:xpar@172.16.11.182:1821/xedm', echo=True)
    meta = MetaData()
    # 这句话就提供了一个表名，其他的，sqlalchemy都帮你做完了
    t = Table("TIMP_DATASOURCE_NOTIFY", meta, autoload=True, autoload_with=db_engine)
    t2= Table("tcalendar_wkday", meta, autoload=True, autoload_with=db_engine)
    class TIMP_DATASOURCE_NOTIFY(object):
        pass
    notifymapper = mapper(TIMP_DATASOURCE_NOTIFY, t)
    DBSession = sessionmaker(bind=db_engine)
    session = DBSession()
    #查询已经读取过的最大钱滚滚接口文件日期
    filedateRow=session.query(TIMP_DATASOURCE_NOTIFY).filter("s_code='FROM_QIANGUNGUN'").order_by(desc(TIMP_DATASOURCE_NOTIFY.beg_date)).first()
    lastLoadDate=filedateRow.beg_date
    # print lastLoadDate
    session.close()

    db_engine = create_engine('oracle://xedm_dm:xpar@172.16.11.182:1821/xedm', echo=True)
    meta = MetaData()
    # 这句话就提供了一个表名，其他的，sqlalchemy都帮你做完了
    t = Table("dim_time", meta, autoload=True, autoload_with=db_engine)
    class dim_time(object):
        pass
    notifymapper = mapper(dim_time, t)
    DBSession = sessionmaker(bind=db_engine)
    session = DBSession()
    #查询已经读取过的最大钱滚滚接口文件日期
    dateRow=session.query(dim_time).filter(text("lastwkdate=:date")).params(date=lastLoadDate).order_by(dim_time.lastwkdate).first()
    lastLoadDate=dateRow.bk_date
    session.close()
    return lastLoadDate

def writelog(errmsg):
    output = open('..\log.txt', 'a')
    output.write(str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))) +'  '+errmsg+'\n')
    output.close()

def ftp_down(fileprefix,ftpfiledate):
    ftp=FTP()
    ftp.set_debuglevel(2)#打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.connect('172.16.11.184','21')#连接
    ftp.login('test','test')#登录，如果匿名登录则用空串代替即可
    bufsize = 1024#设置缓冲块大小
    #判断是否指定日期的OK文件已经存在
    okFileName=ftpfiledate+'_ok.txt'
    try:
        ftp.retrbinary('RETR %s' % okFileName,open(okFileName, 'wb').write)
    except Exception,e:
        return False
    ftpfilename =fileprefix+ftpfiledate+r'.zip'
    file_handler = open(ftpfilename,'wb')#以读模式在本地打开文件
    ftp.retrbinary('RETR %s' % ftpfilename,file_handler.write,bufsize)#上传文件
    #ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    writelog(ftpfilename+"  is ftp down successfully \n")
    return True
def unzipAndDecrypt(zipfilename,filedate):
    '''
    解密的同时，进行解压
    :param localfilename: 指定的加密后ZIP文件
    :return:成功返回True,失败返回False
    '''
    try:
        #winrar e WAREHOURSE_QGG_20160811.zip * 20160811\ -y -p12345678
        commandstr = r'winrar e '+zipfilename+r' * '+filedate + r'\ -y -p12345678'
        os.system(commandstr)
    except Exception,e:
        return false
    return true

#############################主程序开始###############################
##1.获取当前需要加载的数据日期
fileprefix='WAREHOURSE_QGG_'
rawdate='2016-08-11'
# rawdate=get_load_date()
date=rawdate.replace('-','')
zipfileName=fileprefix+date+r'.zip'
##2，启动循环，每10分钟轮循一次指定日期的文件是否存在
while(true):
    if(ftp_down(fileprefix,date)):
        writelog(date+" zip file is ftp down successfully \n")
        break
    time.sleep(600)
##3,解压并解密对应的文件夹,生成指定的文件夹
if unzipAndDecrypt(zipfileName,date):
    writelog(date+" zip file is unzip and decrypt successfully \n")
else:
    writelog(date+' unzip error!')
##4,将衡泰schema.ini文件考到 date 命名的文件夹当中,
    # winrar e WAREHOURSE_QGG_20160811.zip * 20160811\ -y -p12345678
commandstr = r'copy '+r' schema.ini '+date
os.system(commandstr)
##5,将信号数据插入到衡泰的信号表当中,
add_signal(rawdate)
writelog(date+' 插入信号数据成功')