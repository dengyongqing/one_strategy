import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np

def start():
    get_k_data = ts.get_k_data("sh000001", start='1990-12-19');
    data = pd.DataFrame(get_k_data);
    data = data[data.date > "2017-08-01"]
    print(data.iloc[:,0].size)

start();