from rqalpha.api import *
import tushare as ts
import pandas as pd
import time
import talib

import talib as ta
import numpy as np


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):

    # 选择我们感兴趣的股票
    # context.s1 = "000001.XSHE"
    # context.s1 = "000651.XSHE"
    context.s1 = "300409.XSHE"
    
    # context.s2 = "601988.XSHG"
    # context.s3 = "000068.XSHE"
    context.stocks = [context.s1]

    context.TIME_PERIOD = 14
    context.HIGH_RSI = 85
    context.LOW_RSI = 30
    context.ORDER_PERCENT = 0.3

    # get_k_data = ts.get_k_data("sh000001", start='1990-12-19');
    # get_k_data = ts.get_k_data("sz300409", start='1990-12-19');
    # get_k_data = ts.get_k_data("sh000001", start='2016-12-10');
    # get_k_data = ts.get_k_data("sz000651", start='2014-12-10');
    get_k_data = ts.get_k_data("sz300409", start='2014-12-10');
    
    context.data = pd.DataFrame(get_k_data);
    data = context.data;

    up_list = [];
    up_list_bak = [];
    down_list = [];
    up_down_list = [];
    per_volume_list = [];
    up_date_list = [];
    down_date_list = [];
    date_list = [];
    close_list = [];
    volume_list = [];
    qhlsr_list = [];
    obv_list = [];
    obv_rate_list = [];
    obv = 0;

    super_v_list = [];

    times = 100000000;
    up_volume = 1;
    down_volume = 1;

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
        temp_index = index - 2;
        
        

        up_list.append(times * (close - y_close)/volume);
        down_list.append(times * (high - close) / volume);
        up_down_list.append(times * (close - y_close)/volume - times * (high - close) / volume);
        

        

        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;

    up_list = ta.EMA(np.array(up_list), 20)
    context.up_list = up_list;
    context.up_down_list = up_down_list;

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    
    # 开始编写你的主要的算法逻辑
    bar_date = bar_dict[context.s1].datetime.strftime( "%Y-%m-%d")
    
    data = context.data
    data = data[data.date < bar_date]
    data_size = data.iloc[:,0].size;

    up_down_list = context.up_down_list;
    up_list = context.up_list;

    index = (data_size - 1);

    if index > 2 :

        flag9 = (up_list[index] > 1);
        flag10 = (up_list[index] < 1);

        # 计算现在portfolio中股票的仓位
        cur_position = context.portfolio.positions[context.s1].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close

        if flag9: 
            # 满仓入股
            order_percent(context.s1, 1)
            # order_target_value(context.s1, 1)
            print("满仓买入")
        elif flag10:
            # order_percent(context.s1, -1)
            # order_percent(context.s1, 0)
            order_target_value(context.s1, 0)
            print("清仓卖出")
    
    
    ###阻力指标


    # up_times = 0;
    # all_times = 0;
    # max_length = len(up_list);
    # y_close = 0;
    # for index, row in data.iterrows():
    #     # if (max_length-1) >= index :
    #         # open = data["open"][index + 1];      
    #         # close = data["close"][index + 1];

    #         # open = data["open"][index + 1];      
    #         # close = data["close"][index + 1];
        
    #     volume = row.volume;
    #     date = row.date;
    #     # flag1 = (up_list[index] > up_list[index-1]);
    #     # flag2 = (down_list[index] < down_list[index-1]);
    #     flag3 = (up_down_list[index] > up_down_list[index - 1] > 1.5);
    #     flag4 = (obv_rate_list[index] > obv_rate_list[index - 1] > 1.3);
    #     flag5 = (qhlsr_list[index] > qhlsr_list[index-1] > 1);

    #     flag6 = (up_down_list[index] < 1);
    #     flag7 = (obv_rate_list[index] < 1.2);
    #     flag8 = (qhlsr_list[index] < 1);

    #     # 计算现在portfolio中股票的仓位
    #     cur_position = context.portfolio.positions[context.s1].quantity
    #     # 计算现在portfolio中的现金可以购买多少股票
    #     shares = context.portfolio.cash / bar_dict[context.s1].close

    #     if max_length > index and flag3 and flag4 and flag5: 
    #         # 满仓入股
    #         order_shares(context.s1, shares)
    #         all_times = all_times + 1;
    #         # if close > data["close"][index] :   
    #         #     up_times = up_times + 1;
        
    #     if flag6 or flag7 or flag8:
    #         order_target_value(context.s1, 0)
    #     y_close = data["close"][index];  
    
    # print(up_times);
    # print(all_times);
    # print(max_length);
    # print(up_times / all_times);









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