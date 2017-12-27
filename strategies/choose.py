# -*- coding:utf-8 -*-  
from sqlalchemy import create_engine
from django.http import HttpResponse
import json
import pandas as pd
import numpy as np
import tushare as ts
import time,sched
import schedule
import time
import datetime
import queue
import threading

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from mail.mail import send_mail
import smtplib
import json
import random

# 一个选股策略
def choose():
    print("I'm working......选股策略")
    # 股票列表
    engine = create_engine('postgresql://postgres:142857@47.93.193.128:5432/tushare') 
    stock_basics = ts.get_stock_basics()
    data = pd.DataFrame(stock_basics)
    data = data[(data['npr']>30) & (data['gpr']>30) & (data['rev']>20) & (data['profit']>20) & (data['pe']<40)]
    data.to_sql('my_stocks',engine,index=True,if_exists='replace')

    read_sql_query = pd.read_sql_query('select * from my_stocks',con = engine)
    data = pd.DataFrame(read_sql_query)

    # my_stocks = ''
    # for index, row in data.iterrows():   # 获取每行的index、row
    #     my_stocks = my_stocks + '\n' + row.name + '_' + row['name']
    #     print(json.dumps(row['name']))
    # print(data)
    
    send_mail(data, 'choose')

    print("选股策略......done")
