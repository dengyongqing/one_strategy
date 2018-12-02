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

mail_host="smtp.qq.com"  #设置服务器
mail_user="1715620917@qq.com"    #用户名
mail_pass="aagtpoeanndxbigj"   #口令 

sender = ['1715620917@qq.com']
receivers = ['dengyongqing@aliyun.com']
# receivers = [
#     'dengyongqing@aliyun.com', 
#     '1148674087@qq.com',    #邓永康
#     '13816904330@163.com', #姜飞标
#     '317223343@qq.com',    #陈贵
#     '312204337@qq.com',    #汤东强
#     '511868788@qq.com',    #田世峰
#     '448943531@qq.com',    #杨少文
#     '196863227@qq.com',    #joshua
#     ]

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
    
    print("***********************************")
    now = get_now()  
    subject = '小安策略' + '(' + now + ')'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        # smtpObj = smtplib.SMTP() 
        # smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号

        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  

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
        # smtpObj = smtplib.SMTP() 
        # smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号

        smtpObj = smtplib.SMTP_SSL(mail_host, 465) 
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
        # smtpObj = smtplib.SMTP() 
        # smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号

        smtpObj = smtplib.SMTP_SSL(mail_host, 465) 
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

    url = "http://47.93.193.128/happy?code=" + code
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
            pb = str(stock.pb) # pd,市净率
            rev = str(stock.rev) # rev,收入同比(%)
            profit = str(stock.profit) # profit,利润同比(%)
            gpr = str(stock.gpr) # gpr,毛利率(%)
            npr = str(stock.npr) # npr,净利润率(%)
            esp = str(stock.esp) # esp,每股收益
            roe = str(stock.roe) # roe,净资产收益率
            
            # profits_yoy = str(stock.profits_yoy) # profits_yoy, 净利润同比
            holders = str(stock.holders) # holders,股东人数
            
            # data = data[(data['npr']>30) & (data['roe']>30) & (data['rev']>20) & (data['profits_yoy']>20) & (data['profit']>20) & (data['pb']<10) & (data['pe']<40)]

            today = get_today()  
            url = "http://47.93.193.128/happy?code=" + code
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
                    市盈率："""+pe+"""
                </p>
                <p>
                    市净率："""+pb+"""
                </p>
                <p>
                    净利润率(%)："""+npr+"""
                </p>
                <p>
                    净资产收益率(%)："""+roe+"""
                </p>

                <p>
                    收入同比(%)："""+rev+"""
                </p>
               
                <p>
                    净利润同比："""+profit+"""
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