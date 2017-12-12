# run_file_demo
from rqalpha import run_file
from rqalpha.utils import scheduler
import schedule
import time

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": False,
    #   "output_file": '/Users/dengyongqing/my_work/one_strategy/examples/result.pkl',
      "plot_save_file": './',
    }
  }
}

strategy_file_path = "/examples/happy.py"
def start():
    run_file(strategy_file_path, config)

start()
schedule.every(1).minutes.do(start)

while 1:
    schedule.run_pending()
    time.sleep(1)