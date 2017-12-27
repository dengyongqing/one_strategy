# -*- coding:utf-8 -*-  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import traceback
import smtplib
import json
import random

import time
import datetime

mail_host="smtp.aliyun.com"  #设置服务器
mail_user="dengyongqing@aliyun.com"    #用户名
mail_pass="Dfzr.Rrqs@1"   #口令 

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr if isinstance(addr, str) else addr))

def send_mail(stock, flag):
    
    # send_mail('dengyongqing@aliyun.com', my_stocks) #邓永庆
    # send_mail('13816904330@163.com', my_stocks) #姜老板
    # send_mail('317223343@qq.com', my_stocks) #陈贵
    # send_mail('312204337@qq.com', my_stocks) #汤东强

    sender = ['dengyongqing@aliyun.com']
    receivers = ['dengyongqing_json@aliyun.com']
    # receivers = ['dengyongqing@aliyun.com', '13816904330@163.com', '317223343@qq.com', '312204337@qq.com']

    for mail in receivers:   # 获取每行的index、row
        try:
            if flag == 'choose':
                # send_choose_mail(sender, receivers, stock)
                print('choose')
            if flag == 'buy': 
                send_buy_mail(sender, receivers, stock)
                print('buy')
            if flag == 'sell': 
                # send_sell_mail(sender, receivers, stock)
                print('sell')
                
        except Exception as e:
            print(e)
    

def send_choose_mail(sender, receivers, stock):
    # from_addr = raw_input('From: ')
    # password = raw_input('Password: ')
    # to_addr = raw_input('To: ')
    # smtp_server = raw_input('SMTP server: ')
    print("I'm working......发送邮件")

    from_addr = 'dengyongqing_json@aliyun.com'
    password = 'Dfzr.Rrqs@1'
    to_addr = 'dengyongqing@aliyun.com'
    smtp_server = 'smtp.aliyun.com'
    # random.uniform(10, 20)
    msg = MIMEText(stocks, 'plain', 'utf-8')
    msg['From'] = _format_addr('长坡厚雪策略 %s' % (from_addr))
    msg['To'] = _format_addr('friends <%s>' % to)
    msg['Subject'] = Header('来自未来的问候……', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to], msg.as_string())
    server.quit()
    print("发送邮件......done")


def send_buy_mail(sender, receivers, stock):
    print("I'm working......发送邮件")
    
    code = stock.code
    name = stock.symbol
    close = stock.close
    datetime = stock.datetime
    today = datetime.strftime('%Y-%m-%d')

    # code = '300059'
    # name = '东方财富'
    # close = '35'
    # datetime = stock.datetime
    # today = '2017-12-26'

    sender = sender
    receivers = receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    url = "http://47.93.193.128/controllers/happy?code=" + code
    mail_msg = """
            <div style="padding: 10px; border: 1px dashed #bbb;">
                <p>
                    股票名称："""+name+"""_"""+code+"""
                </p>
                <p>
                    日期："""+today+"""
                </p>
                <p>
                    收盘价："""+close+"""
                </p>
                <p>
                    操作类型：<span style="color: red;">买入</span>
                </p>
                <p>
                    策略名称：长坡厚雪策略
                </p>
                <p>
                    <span>
                        策略回测结果：
                    </span>
                    <span>
                        <a href="""+url+""">"""+url+"""</a>
                    </span>
                </p>
            </div>
        """
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(mail_user, 'utf-8')
    message['To'] =  Header('小安', 'utf-8')
    
    subject = 'Python SMTP 邮件测试77'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except (smtplib.SMTPException, Exception) as e:
        print (e)
        print ("Error: 无法发送邮件")
    print("发送邮件......done")


def send_sell_mail(sender, receivers, stock):
    # from_addr = raw_input('From: ')
    # password = raw_input('Password: ')
    # to_addr = raw_input('To: ')
    # smtp_server = raw_input('SMTP server: ')
    print("I'm working......发送邮件")

    from_addr = 'dengyongqing_json@aliyun.com'
    password = 'Dfzr.Rrqs@1'
    to_addr = 'dengyongqing@aliyun.com'
    smtp_server = 'smtp.aliyun.com'
    # random.uniform(10, 20)
    msg = MIMEText(stocks, 'plain', 'utf-8')
    msg['From'] = _format_addr('长坡厚雪策略 %s' % (from_addr))
    msg['To'] = _format_addr('friends <%s>' % to)
    msg['Subject'] = Header('来自未来的问候……', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to], msg.as_string())
    server.quit()
    print("发送邮件......done")


def get_temp_text(stock):
    code = stock.code
    name = stock.symbol
__all__ = ['send_mail']