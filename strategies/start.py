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
    for index, row in data.iterrows():   # 获取每行的index、row
        try:
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
              #   "output_file": '/Users/dengyongqing/my_work/one_strategy/examples/result.pkl',
                "plot_save_file": './one_data/static/' + row.code + '.png',
                # "plot_save_file": './static/' + row.code + '.png',
              }
            }
          }
          print('开始生成图片......' + row.code)
          run_file(strategy_file_path, config)
          gc.collect()
          time.sleep(5)
          print('生成图片成功......' + row.code)
        except Exception as e:
          print(e)

start()

schedule.every(5).minutes.do(start)
while 1:
    schedule.run_pending()
    time.sleep(1)