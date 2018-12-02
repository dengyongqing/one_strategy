# run_file_demo
from rqalpha import run_file
from rqalpha.utils import scheduler
import schedule
import time

def add_tag(code):
  if len(code) == 5:
      return code + '.XHKG'
  elif code.startswith('6'):
      return  code + '.XSHG'
  elif code.startswith('3'):
      return code + '.XSHE'
  elif code.startswith('0'):
      return code + '.XSHE'
code="000651";
start_date = "2010-12-10";
temp_context = {"start_date": start_date, 'code': code, 'tagCode': add_tag(code)}
config = {
  "base": {
    # "start_date": "2010-12-10",
    "start_date": temp_context["start_date"],
    "end_date": "2018-05-10",
    # "benchmark": "000001.XSHG",
    # "benchmark": "000651.XSHE",
    "benchmark": temp_context["tagCode"],
    
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
    "context_vars": temp_context,
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True,
    #   "output_file": '/work/one_strategy/examples/result.pkl',
      "plot_save_file": './',
    }
  }
}

strategy_file_path = "./zl.py"
def start():
    run_file(strategy_file_path, config)

start()
schedule.every(1).minutes.do(start)

while 1:
    schedule.run_pending()
    time.sleep(1)
