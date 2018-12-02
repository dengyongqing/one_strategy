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
    v_list = [];
    per_volume_list = [];
    rvi_list = [];
    up_date_list = [];
    down_date_list = [];
    date_list = [];
    close_list = [];
    volume_list = [];
    qhlsr_list = [];
    obv_list = [];
    obv_rate_list = [];
    zzz_v_list = [];
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
        zzz_v_list.append((close - y_close));

        v_list.append(close - y_close);
        up_list.append(times * (close - y_close)/volume);
        print(times * (close - y_close)/volume);
        down_list.append(times * (high - close) / volume);
        up_down_list.append(up_list[index] - down_list[index]);
        # rvi_list.append((close-open)/(high-low));

        if (high-low) == 0 :
            # per_volume_list.append(0);
            rvi_list.append(0);
        else :
            # per_volume_list.append((volume/(close - y_close)));
            rvi_list.append((close-open)/(high-low));
        
        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;

    fig, axes = plt.subplots(3, 1, sharex=True, sharey=False)
    # axes.plot(up_list[0:2300], 'r-')
    # plt.subplots_adjust(wspace = 0, hspace = 0)
    # plt.figure(figsize=(8,4))
    lll = 1000;
    timeperiod = 20;

    obv_list = get_obv(data, data_size - lll, data_size);

    close_ma = ta.MA(np.array(close_list[len(close_list) - lll:len(close_list)]), 1)
    # rvi_ma = ta.EMA(np.array(rvi_list[len(rvi_list) - lll:len(rvi_list)]), timeperiod)
    # up_down_ma = ta.EMA(np.array(up_down_list[len(up_down_list) - lll:len(up_down_list)]), timeperiod)
    rvi_ma = ta.CMO(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod)
    # up_down_ma = ta.ROC(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod)
    s = 50;
    f = 9;
    up_down_ema_s = ta.EMA(np.array(up_list[len(up_list) - lll:len(up_list)]), s)
    up_down_ema_f = ta.EMA(np.array(up_list[len(up_list) - lll:len(up_list)]), f)

    real = ta.LINEARREG_SLOPE(np.array(close_list[len(close_list) - lll:len(close_list)]), timeperiod=10)
    real = ta.EMA(np.array(real), s)

    up_down_ma_s = ta.MA(np.array(up_list[len(up_list) - lll:len(up_list)]), s)
    up_down_ma_f = ta.MA(np.array(up_list[len(up_list) - lll:len(up_list)]), f)

    v_ema_s = ta.EMA(np.array(v_list[len(v_list) - lll:len(v_list)]), s)
    v_ema_f = ta.EMA(np.array(v_list[len(v_list) - lll:len(v_list)]), f)

    axes[0].plot(date_list[len(date_list) - lll:len(date_list)],close_ma,"y--",linewidth=1);
    # axes[0].plot(date_list[len(date_list) - lll:len(date_list)],v_ema_s,"r--",linewidth=1);
    # axes[1].plot(date_list[len(date_list) - lll:len(date_list)],rvi_ma,"b--",linewidth=1);
    axes[1].plot(date_list[len(date_list) - lll:len(date_list)],real,"b--",linewidth=1);
    # axes[1].plot(date_list[len(date_list) - lll:len(date_list)],v_ema_f,"r--",linewidth=1);
    axes[2].plot(date_list[len(date_list) - lll:len(date_list)],up_down_ema_s,"b--",linewidth=1);
    axes[2].plot(date_list[len(date_list) - lll:len(date_list)],up_down_ema_f,"r--",linewidth=1);
    # axes[2].plot(date_list[len(date_list) - lll:len(date_list)],,"b--",linewidth=1);

    where_are_nan = np.isnan(up_down_ema_s)
    where_are_inf = np.isinf(up_down_ema_s)
    up_down_ema_s[where_are_nan] = 0
    up_down_ema_s[where_are_inf] = 0

    
        
    # print("up_list", np.mean(up_down_ema_s));
    # print("v_list", np.mean(v_list));
    plt.show()
   

start();
