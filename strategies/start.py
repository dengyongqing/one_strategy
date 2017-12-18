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
import daemon

from rqalpha.api import *
from rqalpha import run_func

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000538.XSHE"
    update_universe(context.s1)

    context.eps = 2
    # stock_basics = ts.get_stock_basics()
    # data = pd.DataFrame(stock_basics)
    # my_stock = 100000
    # for index, row in data.iterrows():   # 获取每行的index、row
    #     if row.name == context.s1:
    #         my_stock = row

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

   
    eps = context.eps
    close = bar_dict[context.s1].close
    mpe = close / eps
   
    if mpe < 30:
        order_percent(context.s1, 1)
    if mpe > 50:
        order_percent(context.s1, -1)

    # if not context.fired:
    #     # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
    #     order_percent(context.s1, 1)
    #     context.fired = True

def after_trading(context):
    pass


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
            temp_run_file(row)
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
        #   "output_file": '/Users/dengyongqing/my_work/one_strategy/examples/result.pkl',
          "plot_save_file": './one_data/static/' + row.code + '.png',
          # "plot_save_file": './static/' + row.code + '.png',
        }
      }
    }
    print('开始生成图片......' + row.code)
    run_file(strategy_file_path, config)
    run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
    print('生成图片成功......' + row.code)

start()
# 您可以指定您要传递的参数
# run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
    
# schedule.every(5).minutes.do(start)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)