#coding=utf-8
# __author__ = 'xuyuming'
import zipfile
import os
import shutil
from ftplib import FTP
import re
import time
#记录文件日志
def writelog(errmsg):
    output = open('..\log.txt', 'a')
    output.write(str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))) +'  '+errmsg+'\n')
    output.close()

#上传文件
def ftp_up(filename):
    ftp=FTP()
    ftp.set_debuglevel(2)#打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.connect('172.16.150.34','21')#连接
    ftp.login('hadoop','hadoop123')#登录，如果匿名登录则用空串代替即可
    bufsize = 1024#设置缓冲块大小
    file_handler = open(filename,'rb')#以读模式在本地打开文件
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#上传文件
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    writelog(filename+"  is ftp successfully \n")

#1,判断指定文件夹是否存在，将指定的目录下的日期开头的OK文件找到
filePath = r'D:\temp\data'
os.chdir(filePath)#切换工作目录
filelist=os.listdir(filePath)
print filelist
for i in filelist:
    if re.search(r'([0-9]+)_OK\.txt', i, flags=0):
        date= re.search(r'([0-9]+)_OK\.txt', i, flags=0).group(1)
        break
    else:
        errmsg = "no ok file is found"
        writelog(errmsg)
        exit()
#2,压缩指定日期的数据文件，保留OK文件

commandstr = r'winrar a WAREHOURSE_'+date+r'.zip *.txt -p12345678 -r -x*OK.txt -ms zip'
os.system(commandstr)
writelog("zip is done!")
#3,将OK文件和数据文件一起通过FTP上传

ftp_up('WAREHOURSE_'+date+r'.zip')
ftp_up(date+'_OK.txt')
errmsg="ftp is done"
writelog(errmsg)
#将所有的TXT文件归档
for i in filelist:
    if re.search(r'([0-9]+)(.*)\.txt', i, flags=0):
        shutil.move(i,r'..\move\\'+i)

#FTP,记录上传日志，程序退出




