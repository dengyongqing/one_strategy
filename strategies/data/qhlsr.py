import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np

def get_one_obv(h, l, o, c, v, y, y_v):
    try:
        # obv = ((c - l) - (h - c)) * v / (h - l);
        
        obv = ((c - y)) * v / (h - l);

        # if y >= o:
        #     obv = ((c - y)) * v / (h - l);
        # else:
        #     obv = ((c - o)) * v / (h - l);
            
        # if (c > y) :
        #     return abs(obv);
        # elif (c < y) :
        #     return -abs(obv);
        # else :
        #     return 0;

        # if obv == None:
        #     obv = 0;

        # if c <= y : 
        #     return -abs(obv)
        return obv;
    except Exception as e:
        return 0;

def get_obv(data, start, end):
    data_size = data.iloc[:,0].size;
    obv_list = data.iloc[start:end, :];
    obv = 0;
    list = [];
    y_close = 0;
    y_volume = 0;
    for index, row in obv_list.iterrows():
        open = row.open;
        close = row.close;
        high = row.high;
        low = row.low;
        volume = row.volume;
        
        if index == 0 or volume == None:
            obv = obv + 0;
        else: 
            obv = obv + get_one_obv(high, low, open, close, volume, y_close, y_volume);

        if obv < 0:
            print(obv);
        # elif (close > open):
        #     obv = obv + get_one_obv(high, low, open, close, volume, y_close);
        # elif (open > close):
        #     obv = obv - get_one_obv(high, low, open, close, volume, y_close);
        list.append(obv);
        y_close = close;
        y_volume = volume;
            
    return list;

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


    y_open = 0;
    y_close = 0;
    y_high = 0;
    y_low = 0;
    y_volume = 0;

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

        ###能量潮指标

        ###阻力指标
        if y_volume == 0:
            qhlsr = 0
        else:
            qhlsr = (close - y_close) - (volume - y_volume) * (y_high - y_low)/y_volume;
        qhlsr_list.append(qhlsr);
        print(qhlsr)

        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;


        

    # up_times = 0;
    # all_times = 0;
    # max_length = len(up_list);
    # for index, row in data.iterrows():
    #     if (max_length-1) > index :
    #         open = data["open"][index];      
    #         close = data["close"][index];

    #         # open = data["open"][index + 1];      
    #         # close = data["close"][index + 1];
        
    #     volume = row.volume;
    #     date = row.date;
    #     flag1 = (up_list[index] > up_list[index-1]);
    #     flag2 = (down_list[index] < down_list[index-1]);
    #     flag3 = (up_down_list[index] > up_down_list[index - 1] > 0);
    #     flag4 = (up_down_list[index] > 0);
        
    #     if max_length > index and flag1 and flag2 and flag3: 
    #         all_times = all_times + 1;
    #         if close > open :   
    #             up_times = up_times + 1;
        
        # y_close = data["close"][index];  
    
    # print(up_times);
    # print(all_times);
    # print(max_length);
    # print(up_times / all_times);


        
    fig, axes = plt.subplots(2, 1, sharex=True, sharey=False)

    lll = 100;
    timeperiod = 1;

    # obv_list = get_obv(data, len(date_list) - lll, len(date_list));

    qhlsr_ma = ta.MA(np.array(qhlsr_list[len(qhlsr_list) - lll:len(qhlsr_list)]), timeperiod=5)
    close_ma = ta.MA(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod=timeperiod)
    # obv_ma = ta.MA(np.array(obv_list[len(obv_list) - lll:len(obv_list)]), timeperiod=timeperiod)


    axes[0].plot(date_list[len(date_list) - lll:len(date_list)],qhlsr_ma,"r--",linewidth=1);
    # axes[0].plot(date_list[len(date_list) - lll:len(date_list)],obv_ma,"r--",linewidth=1);
    axes[1].plot(date_list[len(date_list) - lll:len(date_list)],close_ma,"b--",linewidth=1);
    # plt.margins(0)
    
    plt.show()
   

start();
