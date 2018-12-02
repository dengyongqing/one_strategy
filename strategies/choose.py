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
import math
import talib as ta
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 一个选股策略
def choose():
    print("I'm working......选股策略")
    # 股票列表
    engine = create_engine('postgresql://postgres:142857@47.93.193.128:5432/xiaoan') 
    # stock_basics = ts.get_stock_basics()
    temp_stock_basics = pd.read_sql_query('select * from stock_basics_all',con = engine)
    stock_basics = pd.DataFrame(temp_stock_basics)

    data = pd.DataFrame(stock_basics)

    data = data[(data['pe']<40)]    # pe,市盈率
    data = data[(data['pb']<10)]    # pd,市净率

    data = data[(data['npr']>10)]  # npr,净利润率(%)
    data = data[(data['roe']>10)]  # roe,净资产收益率

    data = data[(data['rev']>0)]   # rev,收入同比(%)
    # data = data[(data['profits_yoy'].isnull()) | (data['profits_yoy']>10)]
    data = data[(data['profit']>0)] # profit,利润同比(%)
    
    data.to_sql('my_stocks',engine,index=True,if_exists='replace')

    data = pd.read_sql_query('select * from my_stocks',con = engine)
    data = pd.DataFrame(read_sql_query)

    get_k_data = ts.get_k_data('000651', start='1990-12-19')
    ma5 = ta.MA(get_k_data['close'].values, timeperiod=5, matype=0)
    ma10 = ta.MA(get_k_data['close'].values, timeperiod=10, matype=0)
    ma20 = ta.MA(get_k_data['close'].values, timeperiod=20, matype=0)
    ma60 = ta.MA(get_k_data['close'].values, timeperiod=60, matype=0)
    
    fig, axes = plt.subplots(1, 1, sharex=True, sharey=True)
    # LINEARREG = ta.LINEARREG(get_k_data['close'].values, timeperiod=14)
    real = ta.LINEARREG(get_k_data['close'].values, timeperiod=60)
    get_k_data.set_index('date')
    axes.plot(ma60[1300:2300], 'k-')
    axes.plot(real[1300:2300], 'r-')
    axes.plot(ma60, 'k-')
    plt.subplots_adjust(wspace = 0, hspace = 0)
    # get_k_data.plot(x='date', y='close')

    # x=get_k_data.close 
    # y=get_k_data.close 
    # est=sm.OLS(y,x)
    # est=est.fit()
    # x_prime=np.linspace(x.close.min(), x.close.max(),100)
    # x_prime=sm.add_constant(x_prime)
    # y_hat=est.predict(x_prime)
    # plt.scatter(x.close, y, alpha=0.3)
    # plt.xlabel("Gross National Product")
    # plt.ylabel("Total Employment")
    # plt.plot(x_prime[:,1], y_hat, 'r', alpha=0.9)
    # print(est.summary())
    plt.show()

    # send_mail(data, 'choose')
    print("选股策略......done")


# 均线
def MA():
    print("I'm working......选股策略")
    
    print("选股策略......done")
