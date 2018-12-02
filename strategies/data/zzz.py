import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np

def get_one_obv(h, l, o, c, v, y):
    try:
        # obv = ((c - l) - (h - c)) * v / (h - l);
        
        # obv = ((c - y)) * v / (h - l);

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

        if c == y : 
            return 0;
        elif c < y :
            return -abs(v)
        else:
            return abs(v)
    except Exception as e:
        return 0;

def get_obv(data, start, end):
    data_size = data.iloc[:,0].size;
    obv_list = data.iloc[start:end, :];
    obv = 0;
    list = [];
    y_close = 0;
    for index, row in obv_list.iterrows():
        open = row.open;
        close = row.close;
        high = row.high;
        low = row.low;
        volume = row.volume;
        
        if index == 0 or volume == 0:
            obv = obv + 0;
        else: 
            obv = obv + get_one_obv(high, low, open, close, volume, y_close);

        # elif (close > open):
        #     obv = obv + get_one_obv(high, low, open, close, volume, y_close);
        # elif (open > close):
        #     obv = obv - get_one_obv(high, low, open, close, volume, y_close);
        list.append(obv);
        y_close = close;
            
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
    obv_rate_list = [];
    obv = 0;
    #昨收
    y_close = 0;

    pre_down = 0;
    pre_up = 0;
    times = 100000000;
    up_volume = 1;
    down_volume = 1;

    up_times = 0;

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

        if close > y_close:
            up_times = up_times + 1
            up_volume = up_volume + volume;
        else : 
            down_volume = down_volume + volume;
        obv_rate_list.append(up_volume/down_volume);
        ###阻力指标
        if y_volume == 0:
            qhlsr = 0
        else:
            qhlsr = (close - y_close) - (volume - y_volume) * (y_high - y_low)/y_volume;
        qhlsr_list.append(qhlsr);
        print(qhlsr)


        # print(get_one_obv(high, low, open, close, volume, y_close))
        # obv = obv + get_one_obv(high, low, open, close, volume, y_close);
        #zzz指标

        # if (close == open):
        #     up_list.append(0);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(0 - times * (high - close) / volume);
        # else:
        #     up_list.append(times * (close - low) / volume);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(times * (close - low) / volume - times * (high - close) / volume);

        # if (close == open):
        #     up_list.append(times * (high - low) / volume);
        #     down_list.append(times * (high - low) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # elif (close > open):
        #     up_list.append(times * (high - low) / volume);
        #     down_list.append(times * (high - close + open - low) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # elif (open > close):
        #     down_list.append(times * (high - low) / volume);
        #     up_list.append(times * (high - open + close - low) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);

        # up_list.append(times * (close - low) / volume);
        # down_list.append(times * (high - close) / volume);
        # up_down_list.append(up_list[index] - down_list[index]);


        # up_list.append(times * (close - y_close)/volume);
        # down_list.append(times * (y_close - close) / volume);
        # up_down_list.append(up_list[index] - down_list[index]);

        up_list.append(times * (close - y_close)/volume);
        down_list.append(times * (high - close) / volume);
        up_down_list.append(up_list[index] - down_list[index]);

        # if (close == y_close):
        #     up_list.append(times * (close - y_close)/volume);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # elif (close > y_close):
        #     up_list.append(times * (close - y_close) / volume);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # elif (close < y_close):
        #     up_list.append(times * (close - y_close)/volume);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # else:
        #     print("else")

        # if (close == open):
        #     up_list.append(0);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(0 - times * (high - close) / volume);
        # elif (close > open):
        #     up_list.append(times * (close - open) / volume);
        #     down_list.append(times * (high - close) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # elif (open > close):
        #     down_list.append(times * (open - close) / volume);
        #     up_list.append(times * (close - low) / volume);
        #     up_down_list.append(up_list[index] - down_list[index]);
        # else:
        #     print("else")


        ###能量潮指标

        ###阻力指标
        # (close - y_close)/  (y_high - )

        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;


        

    up_times = 0;
    all_times = 0;
    max_length = len(up_list);
    y_close = 0;
    for index, row in data.iterrows():
        if (max_length-1) >= index :
            open = data["open"][index + 1];      
            close = data["close"][index + 1];

            # open = data["open"][index + 1];      
            # close = data["close"][index + 1];
        
        volume = row.volume;
        date = row.date;
        # flag1 = (up_list[index] > up_list[index-1]);
        # flag2 = (down_list[index] < down_list[index-1]);
        flag3 = (up_down_list[index] > up_down_list[index - 1] > 1.5);
        flag4 = (obv_rate_list[index] > obv_rate_list[index - 1] > 1.3);
        flag5 = (qhlsr_list[index] > qhlsr_list[index-1] > 1);
        
        if max_length > index and flag3 and flag4 and flag5: 
            all_times = all_times + 1;
            if close > data["close"][index] :   
                up_times = up_times + 1;
        
        y_close = data["close"][index];  
    
    print(up_times);
    print(all_times);
    print(max_length);
    print(up_times / all_times);


        
    fig, axes = plt.subplots(4, 1, sharex=True, sharey=False)
    # axes.plot(up_list[0:2300], 'r-')
    # plt.subplots_adjust(wspace = 0, hspace = 0)
    # plt.figure(figsize=(8,4))
    lll = 500;
    timeperiod = 3;

    obv_list = get_obv(data, data_size - lll, data_size);

    up_ma = ta.MA(np.array(up_list[len(up_list) - lll:len(up_list)]), timeperiod=timeperiod)
    down_ma = ta.MA(np.array(down_list[len(down_list) - lll:len(down_list)]), timeperiod=timeperiod)
    close_ma = ta.MA(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod=1)
    up_down_ma = ta.MA(np.array(up_down_list[len(up_down_list) - lll:len(up_down_list)]), timeperiod=timeperiod)
    obv_ma = ta.MA(np.array(obv_list[len(obv_list) - lll:len(obv_list)]), timeperiod=timeperiod)
    qhlsr_ma = ta.MA(np.array(qhlsr_list[len(qhlsr_list) - lll:len(qhlsr_list)]), timeperiod=timeperiod)
    obv_rate_list_ma = ta.MA(np.array(obv_rate_list[len(obv_rate_list) - lll:len(obv_rate_list)]), timeperiod=timeperiod)

   
    # up_ma5 = up_list[len(up_list) - 20:len(up_list)];
    # down_ma5 = down_list[len(down_list) - 20:len(down_list)]

    # axes[0].plot(date_list[len(date_list) - lll:len(date_list)],up_ma5,"r--",linewidth=1);
    # axes[0].plot(date_list[len(date_list) - lll:len(date_list)],down_ma5,"g--",linewidth=1);

    
    # axes[0].plot(date_list[len(date_list) - lll:len(date_list)],obv_ma,"r--",linewidth=1);
    axes[0].plot(date_list[len(date_list) - lll:len(date_list)],qhlsr_ma,"y--",linewidth=1);
    axes[1].plot(date_list[len(date_list) - lll:len(date_list)],up_down_ma,"g--",linewidth=1);
    axes[2].plot(date_list[len(date_list) - lll:len(date_list)],obv_rate_list_ma,"r--",linewidth=1);
    axes[3].plot(date_list[len(date_list) - lll:len(date_list)],close_ma,"b--",linewidth=1);
    # plt.margins(0)
    # print(up_times/len(date_list))
    # print(up_volume/down_volume)
    plt.show()
   

start();
