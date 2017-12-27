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

sender = ['dengyongqing@aliyun.com']
# receivers = ['dengyongqing_json@aliyun.com']
receivers = ['dengyongqing_json@aliyun.com', '13816904330@163.com', '317223343@qq.com', '312204337@qq.com']

def send_mail(stock, flag):
    for mail in receivers:   # 获取每行的index、row
        try:
            if flag == 'choose':
                send_choose_mail(sender, mail, stock)
            if flag == 'buy': 
                send_buy_mail(sender, mail, stock)
            if flag == 'sell': 
                send_sell_mail(sender, mail, stock)
                
        except Exception as e:
            print(e)
    
def send_choose_mail(sender, receivers, stocks):
    print("I'm working......发送选股邮件")

    mail_msg = ''
    # for index, row in stocks.iterrows():   # 获取每行的index、row
    mail_msg = get_choose_temp(stocks, 'buy')
        # mail_msg = mail_msg + row_msg

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = formataddr(["小安", "dengyongqing@aliyun.com"])
    message['To'] =  Header('小安', 'utf-8')
    
    now = get_now()  
    subject = '小安策略' + '(' + now + ')'
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


def send_buy_mail(sender, receivers, stock):
    print("I'm working......发送买入邮件")

    mail_msg = get_trade_temp(stock, 'buy')

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(mail_user, 'utf-8')
    message['To'] =  Header('小安', 'utf-8')
    
    now = get_now()  
    subject = '小安策略' + '(' + now + ')'
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
    print("I'm working......发送卖出邮件")

    mail_msg = get_trade_temp(stock, 'sell')

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(mail_user, 'utf-8')
    message['To'] =  Header('小安', 'utf-8')
    
    now = get_now()  
    subject = '小安策略' + '(' + now + ')'
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


def get_trade_temp(stock, flag):
    code = stock.code
    name = stock.symbol
    close = stock.close
    datetime = stock.datetime
    today = datetime.strftime('%Y-%m-%d')

    url = "http://47.93.193.128/controllers/happy?code=" + code
    msg = """
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
                    操作类型：<span style="color: red;">"""+('买入' if flag == 'buy' else '卖出')+"""</span>
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
    return msg

def get_choose_temp(stocks, flag):
    mail_msg = ''
    try:
        for index, stock in stocks.iterrows():   # 获取每行的index、row
            code = str(stock.code)
            name = str(stock['name'])

            pe = str(stock.pe) # pe,市盈率
            rev = str(stock.rev) # rev,收入同比(%)
            profit = str(stock.profit) # profit,利润同比(%)
            close = str(stock.profit) # 收盘价
            gpr = str(stock.gpr) # gpr,毛利率(%)
            npr = str(stock.npr) # npr,净利润率(%)
            esp = str(stock.esp) # esp,每股收益
            holders = str(stock.holders) # holders,股东人数
            
            today = get_today()  
            url = "http://47.93.193.128/controllers/happy?code=" + code
            msg = """
            <div style="padding: 10px; border: 1px dashed #bbb; margin-bottom: 20px;">
                <p>
                    股票名称："""+name+"""
                </p>
                <p>
                    股票代码："""+code+"""
                </p>
                <p>
                    日期："""+today+"""
                </p>
                <p>
                    收盘价："""+close+"""
                </p>
                <p>
                    市盈率："""+pe+"""
                </p>
                <p>
                    收入同比(%)："""+rev+"""
                </p>
                <p>
                    毛利率(%)："""+gpr+"""
                </p>
                <p>
                    净利润率(%)："""+npr+"""
                </p>
                <p>
                    每股收益："""+esp+"""
                </p>
                <p>
                    股东人数："""+holders+"""
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
            mail_msg += msg

        mail_msg = """
                <div>
                    """+mail_msg+"""
                </div>
            """
        return mail_msg
    except Exception as e:
            print(e)
    
def get_now():
    now = datetime.datetime.now()
    year = int(now.strftime('%Y'))  
    format_now = now.strftime('%Y-%m-%d %H:%M:%S') 
    return format_now

def get_today():
    now = datetime.datetime.now()
    year = int(now.strftime('%Y'))  
    today = now.strftime('%Y-%m-%d') 
    return today

__all__ = ['send_mail']