import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np

def start():
    get_k_data = ts.get_k_data("sh000001", start='1990-12-19');
    data = pd.DataFrame(get_k_data);
    data_size = data.iloc[:,0].size;
    up_list = [];
    down_list = [];
    up_down_list = [];
    up_date_list = [];
    down_date_list = [];
    date_list = [];
    close_list = [];
    volume_list = [];
    qhlsr_list = [];
    obv_list = [];
    obv = 0;
    #昨收
    y_close = 0;

    pre_down = 0;
    pre_up = 0;
    times = 100000000;

    #提取收盘价
    closed=data['close'].values
    
    upper,middle,lower=ta.BBANDS(closed,matype=ta.MA_Type.T3)
    
    print(upper,middle,lower)
    # plt.plot(upper)
    # plt.plot(middle)
    # plt.plot(lower)
    # plt.grid()
    # plt.show()
    diff1=upper-middle
    diff2=middle-lower
    print(diff1)
    print(diff2)

    for index, row in data.iterrows():
        open = row.open;
        close = row.close;
        high = row.high;
        low = row.low;

        volume = row.volume;
        date = row.date;
        date_list.append(date);
        close_list.append(close);
        volume_list.append(volume);
        
    fig, axes = plt.subplots(2, 1, sharex=True, sharey=False)
    lll = len(date_list);
    timeperiod = 1;

    close_ma5 = ta.MA(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod=timeperiod)

    # axes[1].plot(close_list[1000: 1100]);
    axes[1].plot(upper[1000: 1100])
    axes[1].plot(middle[1000: 1100])
    axes[1].plot(lower[1000: 1100])

    plt.show()
   

start();
