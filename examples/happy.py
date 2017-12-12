from rqalpha.api import *
import tushare as ts
import pandas as pd

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import json
import random

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000538.XSHE"
    update_universe(context.s1)

    context.eps = 2
    # stock_basics = ts.get_stock_basics()
    # data = pd.DataFrame(stock_basics)
    # my_stock = 100000
    # for index, row in data.iterrows():   # 获取每行的index、row
    #     if row.name == context.s1:
    #         my_stock = row

    # 是否已发送了order
    context.fired = False

def before_trading(context):
    pass

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

   
    eps = context.eps
    close = bar_dict[context.s1].close
    mpe = close / eps
   
    if mpe < 30:
        order_percent(context.s1, 1)
    if mpe > 50:
        order_percent(context.s1, -1)

    # if not context.fired:
    #     # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
    #     order_percent(context.s1, 1)
    #     context.fired = True

def after_trading(context):
    pass

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
   
