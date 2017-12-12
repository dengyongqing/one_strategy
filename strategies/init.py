# -*- coding:utf-8 -*-  
from sqlalchemy import create_engine
from django.http import HttpResponse
import json
import pandas as pd
import numpy as np
import tushare as ts
import time,sched
import schedule
import time
import datetime
import Queue
import threading

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import json
import random

now = datetime.datetime.now()
year = int(now.strftime('%Y'))  
today = now.strftime('%Y-%m-%d')  
now = now.strftime("%Y-%m-%d %H:%M:%S")

engine = create_engine('postgresql://postgres:142857@47.93.193.128:5432/tushare') 
# engine = create_engine('postgresql://tushare@localhost:5432/tushare')
# 交易数据
def job_1():
    try:
        print("I'm working......交易数据")
        # 股票列表
        stock_basics = ts.get_stock_basics()
        data = pd.DataFrame(stock_basics)
        data.to_sql('stock_basics',engine,index=True,if_exists='replace')
        count = 1;
        for index, row in data.iterrows():   # 获取每行的index、row
            if_exists = 'append'
            if count == 1: 
                if_exists = 'replace'
            # for col_name in data.columns:
            print("开始获取行情数据......" + row.name)
            get_k_data = ts.get_k_data(row.name, start='1990-12-19')
            myData = pd.DataFrame(get_k_data)
            get_k_data.to_sql('k_data',engine,index=True,if_exists=if_exists)
            print("成功写入行情数据......" + row.name)
            count += 1

        # 实时行情
        # today_all = ts.get_today_all()
        # data = pd.DataFrame(today_all)
        # data.to_sql('today_all',engine,index=True,if_exists='replace')
        # print("实时行情......done")

        # # 大盘指数行情列表
        # get_index = df = ts.get_index()
        # data = pd.DataFrame(get_index)
        # data.to_sql('get_index',engine,index=True,if_exists='replace')
        # print("大盘指数行情列表......done")
    except Exception as e:
        print(e)
# 投资参考数据
def job_2():
    try:
        print("I'm working......投资参考数据")
        # 分配预案
        profit_data = ts.profit_data(year, top=1000)
        data = pd.DataFrame(profit_data)
        data.to_sql('profit_data',engine,index=True,if_exists='replace')
        print("分配预案......done")

        # 业绩预告
        forecast_data = ts.forecast_data(year,1)
        data = pd.DataFrame(forecast_data)
        data.to_sql('forecast_data',engine,index=True,if_exists='replace')
        print("业绩预告......done")

        # 限售股解禁
        xsg_data = ts.xsg_data()
        data = pd.DataFrame(xsg_data)
        data.to_sql('xsg_data',engine,index=True,if_exists='replace')
        print("限售股解禁......done")

        # 基金持股
        fund_holdings = ts.fund_holdings(year, 1)
        data = pd.DataFrame(fund_holdings)
        data.to_sql('fund_holdings',engine,index=True,if_exists='replace')
        print("基金持股......done")
    
        # 新股数据
        new_stocks = ts.new_stocks()
        data = pd.DataFrame(new_stocks)
        data.to_sql('new_stocks',engine,index=True,if_exists='replace')
        print("新股数据......done")

        # 融资融券（沪市）
        sh_margins = ts.sh_margins()
        data = pd.DataFrame(sh_margins)
        data.to_sql('sh_margins',engine,index=True,if_exists='replace')
        print("融资融券（沪市）......done")

        # 融资融券（深市）
        sz_margins = ts.sz_margins()
        data = pd.DataFrame(sz_margins)
        data.to_sql('sz_margins',engine,index=True,if_exists='replace')
        print("融资融券（深市）......done")
    except Exception as e:
        print(e)
# 股票分类数据
def job_3():
    try:
        print("I'm working......股票分类数据")
        # 行业分类
        industry_classified = ts.get_industry_classified()
        data = pd.DataFrame(industry_classified)
        data.to_sql('industry_classified',engine,index=True,if_exists='replace')
        print("行业分类......done")

        # 概念分类
        concept_classified = ts.get_concept_classified()
        data = pd.DataFrame(concept_classified)
        data.to_sql('concept_classified',engine,index=True,if_exists='replace')
        print("概念分类......done")

        # 地域分类
        area_classified = ts.get_area_classified()
        data = pd.DataFrame(area_classified)
        data.to_sql('area_classified',engine,index=True,if_exists='replace')
        print("地域分类......done")

        # 中小板分类
        sme_classified = ts.get_sme_classified()
        data = pd.DataFrame(sme_classified)
        data.to_sql('sme_classified',engine,index=True,if_exists='replace')
        print("中小板分类......done")

        # 创业板分类
        gem_classified = ts.get_gem_classified()
        data = pd.DataFrame(gem_classified)
        data.to_sql('gem_classified',engine,index=True,if_exists='replace')
        print("创业板分类......done")

        # # 风险警示板分类
        # st_classified = ts.get_st_classified()
        # data = pd.DataFrame(st_classified)
        # data.to_sql('st_classified',engine,index=True,if_exists='replace')
        # print("风险警示板分类......done")

        # 沪深300成份及权重
        hs300s = ts.get_hs300s()
        data = pd.DataFrame(hs300s)
        data.to_sql('hs300s',engine,index=True,if_exists='replace')
        print("沪深300成份及权重......done")

        # 上证50成份股
        sz50s = ts.get_sz50s()
        data = pd.DataFrame(sz50s)
        data.to_sql('sz50s',engine,index=True,if_exists='replace')
        print("上证50成份股......done")

        # 中证500成份股
        zz500s = ts.get_zz500s()
        data = pd.DataFrame(zz500s)
        data.to_sql('zz500s',engine,index=True,if_exists='replace')
        print("中证500成份股......done")

        # 终止上市股票列表
        terminated = ts.get_terminated()
        data = pd.DataFrame(terminated)
        data.to_sql('terminated',engine,index=True,if_exists='replace')
        print("终止上市股票列表......done")

        # 暂停上市股票列表
        suspended = ts.get_suspended()
        data = pd.DataFrame(suspended)
        data.to_sql('suspended',engine,index=True,if_exists='replace')
        print("暂停上市股票列表......done")
    except Exception as e:
        print(e)

# 基本面数据
def job_4():
    try:
        print("I'm working......基本面数据")

        # 业绩报告（主表）
        report_data = ts.get_report_data(year,1)
        data = pd.DataFrame(report_data)
        data.to_sql('report_data',engine,index=True,if_exists='replace')
        print("业绩报告（主表）......done")

        # 盈利能力
        profit_data = ts.get_profit_data(year,1)
        data = pd.DataFrame(profit_data)
        data.to_sql('profit_data',engine,index=True,if_exists='replace')
        print("盈利能力......done")

        # 营运能力
        operation_data = ts.get_operation_data(year,1)
        data = pd.DataFrame(operation_data)
        data.to_sql('operation_data',engine,index=True,if_exists='replace')
        print("营运能力......done")

        # 成长能力
        growth_data = ts.get_growth_data(year,1)
        data = pd.DataFrame(growth_data)
        data.to_sql('growth_data',engine,index=True,if_exists='replace')
        print("成长能力......done")

        # 偿债能力
        debtpaying_data = ts.get_debtpaying_data(year,1)
        data = pd.DataFrame(debtpaying_data)
        data.to_sql('debtpaying_data',engine,index=True,if_exists='replace')
        print("偿债能力......done")

        # 现金流量
        cashflow_data = ts.get_cashflow_data(year,1)
        data = pd.DataFrame(cashflow_data)
        data.to_sql('cashflow_data',engine,index=True,if_exists='replace')
        print("现金流量......done")

        # 股票列表
        stock_basics = ts.get_stock_basics()
        data = pd.DataFrame(stock_basics)
        data.to_sql('stock_basics',engine,index=True,if_exists='replace')
        print("股票列表......done")
    except Exception as e:
        print(e)
# 宏观经济数据
def job_5():
    try:
        print("I'm working......宏观经济数据")
        # 存款利率
        deposit_rate = ts.get_deposit_rate()
        data = pd.DataFrame(deposit_rate)
        data.to_sql('deposit_rate',engine,index=True,if_exists='replace')
        print("存款利率......done")

        # 贷款利率
        loan_rate = ts.get_loan_rate()
        data = pd.DataFrame(loan_rate)
        data.to_sql('loan_rate',engine,index=True,if_exists='replace')
        print("贷款利率......done")

        # 存款准备金率
        rrr = ts.get_rrr()
        data = pd.DataFrame(rrr)
        data.to_sql('rrr',engine,index=True,if_exists='replace')
        print("存款准备金率......done")

        # 货币供应量
        money_supply = ts.get_money_supply()
        data = pd.DataFrame(money_supply)
        data.to_sql('money_supply',engine,index=True,if_exists='replace')
        print("货币供应量......done")

        # 货币供应量(年底余额)
        money_supply_bal = ts.get_money_supply_bal()
        data = pd.DataFrame(money_supply_bal)
        data.to_sql('money_supply_bal',engine,index=True,if_exists='replace')
        print("货币供应量(年底余额)......done")

        # 国内生产总值(年度)
        gdp_year = ts.get_gdp_year()
        data = pd.DataFrame(gdp_year)
        data.to_sql('gdp_year',engine,index=True,if_exists='replace')
        print("国内生产总值(年度)......done")

        # 国内生产总值(季度)
        gdp_quarter = ts.get_gdp_quarter()
        data = pd.DataFrame(gdp_quarter)
        data.to_sql('gdp_quarter',engine,index=True,if_exists='replace')
        print("国内生产总值(季度)......done")

        # 三大需求对GDP贡献
        gdp_for = ts.get_gdp_for()
        data = pd.DataFrame(gdp_for)
        data.to_sql('gdp_for',engine,index=True,if_exists='replace')
        print("三大需求对GDP贡献......done")

        # 三大产业对GDP拉动
        gdp_pull = ts.get_gdp_pull()
        data = pd.DataFrame(gdp_pull)
        data.to_sql('gdp_pull',engine,index=True,if_exists='replace')
        print("三大产业对GDP拉动......done")

        # 三大产业贡献率
        gdp_contrib = ts.get_gdp_contrib()
        data = pd.DataFrame(gdp_contrib)
        data.to_sql('gdp_contrib',engine,index=True,if_exists='replace')
        print("三大产业贡献率......done")

        # 居民消费价格指数
        cpi = ts.get_cpi()
        data = pd.DataFrame(cpi)
        data.to_sql('cpi',engine,index=True,if_exists='replace')
        print("居民消费价格指数......done")

        # 工业品出厂价格指数
        ppi = ts.get_ppi()
        data = pd.DataFrame(ppi)
        data.to_sql('ppi',engine,index=True,if_exists='replace')
        print("工业品出厂价格指数......done")

    except Exception as e:
        print(e)

# 新闻事件数据
def job_6():
    try:
        print("I'm working......新闻事件数据")
        # 即时新闻
        latest_news = ts.get_latest_news()
        data = pd.DataFrame(latest_news)
        data.to_sql('latest_news',engine,index=True,if_exists='replace')
        print("即时新闻......done")

        # 信息地雷
        notices = ts.get_notices()
        data = pd.DataFrame(notices)
        data.to_sql('notices',engine,index=True,if_exists='replace')
        print("信息地雷......done")

        # 新浪股吧
        guba_sina = ts.guba_sina()
        data = pd.DataFrame(guba_sina)
        data.to_sql('guba_sina',engine,index=True,if_exists='replace')
        print("新浪股吧......done")
    except Exception as e:
        print(e)
# 龙虎榜数据
def job_7():
    try:
        print("I'm working......龙虎榜数据")
        # 每日龙虎榜列表
        top_list = ts.top_list(today)
        data = pd.DataFrame(top_list)
        data.to_sql('top_list',engine,index=True,if_exists='replace')
        print("每日龙虎榜列表......done")

        # 个股上榜统计
        cap_tops = ts.cap_tops()
        data = pd.DataFrame(cap_tops)
        data.to_sql('cap_tops',engine,index=True,if_exists='replace')
        print("个股上榜统计......done")

        # 营业部上榜统计
        broker_tops = ts.broker_tops()
        data = pd.DataFrame(broker_tops)
        data.to_sql('broker_tops',engine,index=True,if_exists='replace')
        print("营业部上榜统计......done")

        # 机构席位追踪
        inst_tops = ts.inst_tops()
        data = pd.DataFrame(inst_tops)
        data.to_sql('inst_tops',engine,index=True,if_exists='replace')
        print("机构席位追踪......done")

        # 机构成交明细
        inst_detail = ts.inst_detail()
        data = pd.DataFrame(inst_detail)
        data.to_sql('inst_detail',engine,index=True,if_exists='replace')
        print("机构成交明细......done")
    except Exception as e:
        print(e)
# 银行间同业拆放利率
def job_8():
    try:
        print("I'm working......银行间同业拆放利率")
        # Shibor拆放利率
        shibor_data = ts.shibor_data()
        data = pd.DataFrame(shibor_data)
        data.to_sql('shibor_data',engine,index=True,if_exists='replace')
        print("银行间同业拆放利率......done")

        # 银行报价数据
        shibor_quote_data = ts.shibor_quote_data()
        data = pd.DataFrame(shibor_quote_data)
        data.to_sql('shibor_quote_data',engine,index=True,if_exists='replace')
        print("银行报价数据......done")

        # Shibor均值数据
        shibor_ma_data = ts.shibor_ma_data()
        data = pd.DataFrame(shibor_ma_data)
        data.to_sql('shibor_ma_data',engine,index=True,if_exists='replace')
        print("Shibor均值数据......done")

        # 贷款基础利率（LPR）
        lpr_data = ts.lpr_data()
        data = pd.DataFrame(lpr_data)
        data.to_sql('lpr_data',engine,index=True,if_exists='replace')
        print("贷款基础利率......done")

        # LPR均值数据
        lpr_ma_data = ts.lpr_ma_data()
        data = pd.DataFrame(lpr_ma_data)
        data.to_sql('lpr_ma_data',engine,index=True,if_exists='replace')
        print("LPR均值数据......done")
    except Exception as e:
        print(e)
# 电影票房
def job_9():
    try:
        print("I'm working......电影票房")
        # 实时票房
        realtime_boxoffice = ts.realtime_boxoffice()
        data = pd.DataFrame(realtime_boxoffice)
        data.to_sql('realtime_boxoffice',engine,index=True,if_exists='replace')
        print("实时票房......done")

        # 每日票房
        day_boxoffice = ts.day_boxoffice()
        data = pd.DataFrame(day_boxoffice)
        data.to_sql('day_boxoffice',engine,index=True,if_exists='replace')
        print("每日票房......done")

        # 月度票房
        month_boxoffice = ts.month_boxoffice()
        data = pd.DataFrame(month_boxoffice)
        data.to_sql('month_boxoffice',engine,index=True,if_exists='replace')
        print("月度票房......done")

        # 影院日度票房
        day_cinema = ts.day_cinema()
        data = pd.DataFrame(day_cinema)
        data.to_sql('day_cinema',engine,index=True,if_exists='replace')
        print("影院日度票房......done")
    except Exception as e:
        print(e)

# 一个选股策略
def job_10():
    print("I'm working......选股策略")
    # 股票列表
    stock_basics = ts.get_stock_basics()
    data = pd.DataFrame(stock_basics)
    data = data[(data['npr']>30) & (data['gpr']>30) & (data['rev']>20) & (data['profit']>20) & (data['pe']<40)]
    data.to_sql('my_stocks',engine,index=True,if_exists='replace')

    my_stocks = ''
    for index, row in data.iterrows():   # 获取每行的index、row
        my_stocks = my_stocks + '\n' + row.name + '_' + row['name']
        print(json.dumps(row['name']))
    # print(my_stocks)
   
    send_mail('dengyongqing@aliyun.com', my_stocks) #邓永庆
    send_mail('13816904330@163.com', my_stocks) #姜老板
    send_mail('317223343@qq.com', my_stocks) #陈贵
    send_mail('312204337@qq.com', my_stocks) #汤东强

    print("选股策略......done")

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_mail(to, stocks):
    # from_addr = raw_input('From: ')
    # password = raw_input('Password: ')
    # to_addr = raw_input('To: ')
    # smtp_server = raw_input('SMTP server: ')
    print("I'm working......发送邮件")

    from_addr = 'dengyongqing_json@aliyun.com'
    password = 'Dfzr.Rrqs@1'
    to_addr = 'dengyongqing@aliyun.com'
    smtp_server = 'smtp.aliyun.com'
    # random.uniform(10, 20)
    msg = MIMEText(stocks, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'小安策略 %s' % (from_addr))
    msg['To'] = _format_addr(u'friends <%s>' % to)
    msg['Subject'] = Header(u'来自未来的问候……', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to], msg.as_string())
    server.quit()
    print("发送邮件......done")
   

# 开始任务
def start():
    print("I'm working......start")
    work()

# 结束任务
def stop():
    print("I'm working......stop")
    schedule.clear('my_job')

def work():
    try:
        print("I'm working......work")
        schedule.every().day.at("17:00").do(job_10).tag('my_job')
        schedule.every().day.at("17:00").do(job_2).tag('my_job')
        schedule.every().day.at("17:00").do(job_3).tag('my_job')
        schedule.every().day.at("17:00").do(job_4).tag('my_job')
        schedule.every().day.at("17:00").do(job_5).tag('my_job')
        schedule.every().day.at("17:00").do(job_6).tag('my_job')
        schedule.every().day.at("17:00").do(job_7).tag('my_job')
        schedule.every().day.at("17:00").do(job_8).tag('my_job')
        schedule.every().day.at("17:00").do(job_9).tag('my_job')
        schedule.every().day.at("17:00").do(job_1).tag('my_job')
    except Exception as e:
        print(e)

def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()

def init():
    jobqueue = Queue.Queue()

    # worker_thread = threading.Thread(target=worker_main)
    # worker_thread.start()

    work()
    # job_10()
    job_1()
    job_2()
    job_3()
    job_4()
    job_5()
    job_6()
    job_7()
    job_8()
    job_9()

    while 1:
        schedule.run_pending()
        time.sleep(1)

