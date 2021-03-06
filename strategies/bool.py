# -*- coding:utf-8 -*-  
from rqalpha.api import *
import tushare as ts
import pandas as pd

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import time
import datetime
import smtplib
import json
import random
import sys, os

# 上证（XSHG）和深圳（XSHE）交易的证券以及港股（XHKG）
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000300.XSHG"
    update_universe(context.s1)

    now = datetime.datetime.now()
    year = int(now.strftime('%Y'))  
    today = now.strftime('%Y-%m-%d')  
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    context.today = today

    # 是否已发送了order
    context.fired = False
    

def before_trading(context):
    pass

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    esp = context.esp
    code = context.code
    stock = bar_dict[code]
    stock.code = code
    close = stock.close
    datetime = stock.datetime
    name = stock.symbol
    today = datetime.strftime('%Y-%m-%d')
    mpe = close / esp
    if mpe < 30:
        order_percent(code, 1)
        if (context.today == today and context.projectName == 'one_strategy'):
            print(code + '_' + name + '********************买入')
            from mail.mail import send_mail
            send_mail(stock, 'buy')
    if mpe > 50:
        order_percent(code, -1)
        if (context.today == today and context.projectName == 'one_strategy'):
            print(code + '_' + name + '********************卖出')
            from mail.mail import send_mail
            send_mail(stock, 'sell')

    # if not context.fired:
    #     # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
    #     order_percent(context.s1, 1)
    #     context.fired = True

def after_trading(context):
    
    pass

__all__ = ['init', 'before_trading', 'handle_bar', 'after_trading']



def temp_run_file(row): 
    temp_context = {'esp': row.esp, 'code': add_tag(row.code), 'projectName': settings.PROJECT_NAME}
    config = {
      "base": {
        "start_date": "2010-01-01",
        "end_date": get_today(),
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": row.code,
        }
      },
      "extra": {
        "log_level": "error",
        "user_system_log_disabled": True,
        "context_vars": temp_context,
      },
      "mod": {
        "sys_analyser": {
          "enabled": False,
          "plot": False,
          # "output_file": './one_data/static/' + row.code + '.png',
          "plot_save_file": './one_data/static/' + row.code + '.png',
          # "plot_save_file": './static/' + row.code + '.png',
        }
      }
    }
    print('开始运行策略-------' + row.name)
    run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
    # run_file(strategy_file_path, config)
    print('策略运行成功-------' + row.name)