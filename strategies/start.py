# -*- coding:utf-8 -*-  
# run_file_demo
from rqalpha import run_file
from rqalpha.utils import scheduler
from db import DB
from init import init
import schedule
import time
import datetime
import pandas as pd
import gc
from daemon import Daemon

from rqalpha.api import *
from rqalpha import run_func

import sys, os
import threading
import multiprocessing

now = datetime.datetime.now()
year = int(now.strftime('%Y'))  
today = now.strftime('%Y-%m-%d')  
now = now.strftime("%Y-%m-%d %H:%M:%S")

strategy_file_path = "./one_strategy/strategies/happy.py"

def start():
    # init()
    engine = DB.get_conn()
    read_sql_query = pd.read_sql_query('select * from my_stocks',con = engine)
    data = pd.DataFrame(read_sql_query)
    count = 1
    for index, row in data.iterrows():   # 获取每行的index、row
        try:
            # _thread.start_new_thread(temp_run_file(row), ("Thread-" + count, count, ) )
            # time.sleep(10)
            # count += 1
            temp_run_file(row)
            # temp_run_file(row)
        except Exception as e:
          print(e)


def temp_run_file(row): 
    print("*************************")
    config = {
      "base": {
        "start_date": "2010-01-01",
        "end_date": today,
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": row.code,
        }
      },
      "extra": {
        "log_level": "error",
        "user_system_log_disabled": True,
      },
      "mod": {
        "sys_analyser": {
          "enabled": True,
          "plot": False,
          # "output_file": './one_data/static/' + row.code + '.png',
          "plot_save_file": './one_data/static/' + row.code + '.png',
          # "plot_save_file": './static/' + row.code + '.png',
        }
      }
    }
    print('开始生成图片......' + row.code)
    start_time = time.time()
    run_file(strategy_file_path, config)

    while 1:
      end_time = time.time()
      if (end_time - start_time) > 30000:
            break
      if os.path.exists('./one_data/static/' + row.code + '.png'):
            print('生成图片成功......' + row.code)
            break
    # time.sleep(5)
    gc.collect()
    # time.sleep(5)
    # run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
    
if __name__ == '__main__':
      
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)

    engine = DB.get_conn()
    read_sql_query = pd.read_sql_query('select * from my_stocks',con = engine)
    data = pd.DataFrame(read_sql_query)

    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except Exception as e:
        # print ("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    # decouple from parent environment
    # os.chdir("/")
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            # print ("Daemon PID %d" % pid)
            sys.exit(0)
    except Exception as e:
        # print ("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    # start the daemon main loop
    # main()

    for index, row in data.iterrows():   # 获取每行的index、row
        try:
            # _thread.start_new_thread(temp_run_file(row), ("Thread-" + count, count, ) )
            # time.sleep(10)
            # count += 1
            temp_run_file(row)
            # temp_run_file(row)
        except Exception as e:
          print(e)

    # start()
   
# schedule.every(5).minutes.do(start)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)