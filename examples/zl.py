from rqalpha.api import *
import tushare as ts
import pandas as pd
import time
import talib

import talib as ta
import numpy as np

def add_tag(code):
  if len(code) == 5:
      return code + '.XHKG'
  elif code.startswith('6'):
      return  code + '.XSHG'
  elif code.startswith('3'):
      return code + '.XSHE'
  elif code.startswith('0'):
      return code + '.XSHE'

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):

    # 选择我们感兴趣的股票
    # context.s1 = "000001.XSHE"
    # context.s1 = "000651.XSHE"
    code="000651"
    # code="000651"
    # code="600036"
    context.s1 = add_tag(code);
    
    # context.s2 = "601988.XSHG"
    # context.s3 = "000068.XSHE"
    # context.stocks = [context.s1]

    context.TIME_PERIOD = 14
    context.HIGH_RSI = 85
    context.LOW_RSI = 30
    context.ORDER_PERCENT = 0.3

    # get_k_data = ts.get_k_data("sh000001", start='1990-12-19');
    # get_k_data = ts.get_k_data("sz300409", start='1990-12-19');
    # get_k_data = ts.get_k_data("sh000001", start='2016-12-10');
    # get_k_data = ts.get_k_data("sz000651", start='2014-12-10');
    get_k_data = ts.get_k_data("sz"+code, start='2010-12-10');
    
    context.data = pd.DataFrame(get_k_data);
    data = context.data;

    up_list = [];
    v_list = [];
    up_list_ma_s = [];
    up_list_ma_f = [];
    up_list_ema_s = [];
    up_list_ema_f = [];
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
        
        v_list.append(close - y_close);
        up_list.append(times * (close - y_close)/volume);
        down_list.append(times * (high - close) / volume);
        # up_down_list.append(up_list[index] - down_list[index]);
        up_down_list.append(times * (close - y_close)/volume - times * (high - close) / volume);
        

        y_open = open;
        y_close = close;
        y_high = high;
        y_low = low;
        y_volume = volume;
    s = 20;
    f = 9;
    v_list_ema_s = ta.EMA(np.array(v_list), s);
    v_list_ema_f = ta.EMA(np.array(v_list), f);
    
    up_list_ema_s = ta.EMA(np.array(up_list), s)
    up_list_ema_f = ta.EMA(np.array(up_list), f)
    
    up_list_ma_s = ta.EMA(np.array(up_list), s)
    up_list_ma_f = ta.EMA(np.array(up_list), f)

    angle_list_s = ta.LINEARREG_ANGLE(np.array(close_list), 5)
    angle_list_f = ta.LINEARREG_ANGLE(np.array(close_list), 3)
    
    # angle_list_s = ta.EMA(ta.LINEARREG_SLOPE(np.array(close_list), 5), 5)
    # angle_list_f = ta.EMA(ta.LINEARREG_SLOPE(np.array(close_list), 3), 3)

    angle_list_s = ta.EMA(np.array(close_list), 20)
    angle_list_f = ta.EMA(np.array(close_list), 9)

    where_are_nan = np.isnan(up_list_ema_s)
    where_are_inf = np.isinf(up_list_ema_s)
    up_list_ema_s[where_are_nan] = 0
    up_list_ema_s[where_are_inf] = 0

    where_are_nan = np.isnan(up_list_ma_f)
    where_are_inf = np.isinf(up_list_ma_f)
    up_list_ma_f[where_are_nan] = 0
    up_list_ma_f[where_are_inf] = 0

    
    context.up_list = up_list;

    context.v_list_ema_s = v_list_ema_s;
    context.v_list_ema_f = v_list_ema_f;

    context.up_list_ma_s = up_list_ma_s;
    context.up_list_ma_f = up_list_ma_f;

    context.up_list_ema_s = up_list_ema_s;
    context.up_list_ema_f = up_list_ema_f;
    
    context.up_down_list = up_down_list;

    context.close_list = close_list;

    context.angle_list_s = angle_list_s;
    context.angle_list_f = angle_list_f;


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    
    # 开始编写你的主要的算法逻辑
    bar_date = bar_dict[context.s1].datetime.strftime( "%Y-%m-%d")
    
    data = context.data
    data = data[data.date < bar_date]
    data_size = data.iloc[:,0].size;

    up_down_list = context.up_down_list;
    up_list = context.up_list;

    up_list_ma_s = context.up_list_ma_s;
    up_list_ma_f = context.up_list_ma_f;

    up_list_ema_s = context.up_list_ema_s;
    up_list_ema_f = context.up_list_ema_f;

    v_list_ema_s = context.v_list_ema_s;
    v_list_ema_f = context.v_list_ema_f;

    close_list = context.close_list;
    
    angle_list_f = context.angle_list_f;
    angle_list_s = context.angle_list_s;
    
    index = (data_size - 1);

    if index > 0 :
        flag1 = up_list_ema_f[index] > 0 and up_list[index] > 0 and up_list_ma_f[index] > 0;
        flag2 = up_list_ema_s[index] < 0 and up_list_ma_f[index] < 0 and up_list[index] < 0;

        flag3 = (up_list_ema_f[index] > up_list_ema_s[index]) and (up_list_ma_f[index] > up_list_ma_s[index]);
        flag4 = (up_list_ema_f[index] < up_list_ema_s[index]) and (up_list_ma_f[index] < up_list_ma_s[index]);
        
        avg = np.mean(up_list_ema_s);
        std = np.std(up_list_ema_s);

        flag5 = (up_list_ema_s[index] > (std));
        flag6 = (up_list_ema_s[index] < (-std));
        print("avg", avg);
        print("std", std);
        
        flag7 = ((up_list_ema_s[index] > up_list_ma_s[index]) and (up_list_ema_f[index] > up_list_ma_f[index]));
        flag8 = ((up_list_ema_s[index] < up_list_ma_s[index]) and (up_list_ema_f[index] < up_list_ma_f[index]));

        flag9 = (up_list_ema_s[index] > up_list_ma_s[index]) and (up_list_ema_f[index] > up_list_ma_f[index]);
        flag10 = (up_list_ema_s[index] < up_list_ma_s[index]) and (up_list_ema_f[index] < up_list_ma_f[index]);

        # 计算现在portfolio中股票的仓位
        cur_position = context.portfolio.positions[context.s1].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close

        # if flag1: 
        # if flag3 and flag7: 
        if flag5 or index < 20: 
        # if flag7: 
        # if flag9: 
            # 满仓入股
            order_percent(context.s1, 1)
            print("满仓买入")
        # elif flag2:
        # elif flag4 and flag8:
        elif flag6:
        # elif flag8:
        # elif flag10:
            order_percent(context.s1, -1)
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