#coding=utf-8
__author__ = 'xuyuming'

"""
定义常见的函数
Created on 2016/04/16
@author: clark xu
@group :
@contact: clark_xym@163.com
"""


import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import time

def sendmail(mail_from ,mail_to ,mail_body,mail_title,smtpserver,username,passwd,filepath,attachname):
    """
        通过SMTP发送带附件的电子邮件
    Return
    --------
    DataFrame
               mail_from ,发件箱地址
               mail_to ,收到箱地址（支持列表）
               mailbody,邮件正文
               mailtitle,邮件标题
               smtpserver,smtp服务器
               username,发件箱用户名
               passwd,发件人密码
               filepath 附件的绝对路径
    """
    #mail_body='hello, this is the mail content'
    #mail_from='88fly@163.com'
    #mail_to=['mysqld@163.com']
    # 构造MIMEMultipart对象做为根容器
    msg=MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    body=MIMEText(mail_body)
    msg.attach(body)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    part = MIMEBase('application', 'octet-stream')

    # 读入文件内容并格式化，此处文件为当前目录下，也可指定目录 例如：open(r'/tmp/123.txt','rb')
    part.set_payload(open(filepath,'rb').read())
    Encoders.encode_base64(part)
    ## 设置附件头
    part.add_header('Content-Disposition', 'attachment',filename=attachname)
    msg.attach(part)

    # 设置根容器属性
    msg['Subject']=mail_title
    msg['From']=mail_from
    msg['To']=';'.join(mail_to)
    msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
    #如上得到了格式化后的完整文本msg.as_string()
    #用smtp发送邮件
    smtp=smtplib.SMTP()
    smtp.connect(smtpserver) #smtp.163.com
    smtp.login(username,passwd)
    smtp.sendmail(mail_from,mail_to,msg.as_string())
    smtp.quit()
    print 'ok'

    print 'mail sent!'

