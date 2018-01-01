# -*- coding:utf-8 -*-  
from rqalpha import run_file
from rqalpha.utils import scheduler
from db.db import get_db_connect
# from data.init import init_data
from choose import choose
import schedule
import time
import datetime
import pandas as pd
import gc

from rqalpha.api import *
from rqalpha import run_func
from happy import *
import settings

import sys, os
import threading
import multiprocessing

from mail.mail import send_mail

strategy_file_path = "./one_strategy/strategies/happy.py"

def start():
    choose()
    engine = get_db_connect()
    read_sql_query = pd.read_sql_query('select * from my_stocks',con = engine)
    data = pd.DataFrame(read_sql_query)
    for index, row in data.iterrows():   # 获取每行的index、row
        try:
            temp_run_file(row)
            time.sleep(15)
            gc.collect()
        except Exception as e:
          print(e)

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
    print('开始运行策略-------' + row.code)
    run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
    # run_file(strategy_file_path, config)
    print('策略运行成功-------' + row.code)

def add_tag(code):
      if len(code) == 5:
          return code + '.XHKG'
      elif code.startswith('6'):
          return  code + '.XSHG'
      elif code.startswith('3'):
          return code + '.XSHE'
      elif code.startswith('0'):
          return code + '.XSHE'

def get_today():
    now = datetime.datetime.now()
    year = int(now.strftime('%Y'))  
    today = now.strftime('%Y-%m-%d') 
    return today


start()
# schedule.every().day.at("17:00").do(start).tag('my_job')
# while 1:
#     schedule.run_pending()
#     time.sleep(1)