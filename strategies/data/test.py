import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib as ta


def start():
    get_k_data = ts.get_k_data("sh000001", start='1990-12-19');
    data = pd.DataFrame(get_k_data);
    data_size = data.iloc[:,0].size;
    date_list = [];
    close_list = [];
    volume_list = [];
    y_close = 0;


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
        
        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;


        
    fig, axes = plt.subplots(2, 1, sharex=True, sharey=False)
    # axes.plot(up_list[0:2300], 'r-')
    # plt.subplots_adjust(wspace = 0, hspace = 0)
    # plt.figure(figsize=(8,4))
    lll = 500;
    timeperiod = 10;


    close_ma = ta.MA(np.array(close_list[len(close_list) - lll:len(close_list)]), 1)
    volume_ma = ta.MA(np.array(volume_list[len(volume_list) - lll:len(volume_list)]), 1)

    axes[0].plot(date_list[len(date_list) - lll:len(date_list)],close_ma,"y--",linewidth=1);
    axes[1].plot(date_list[len(date_list) - lll:len(date_list)],volume_ma,"b--",linewidth=1);
    plt.show()
   

start();
