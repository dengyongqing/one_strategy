# -*- coding:utf-8 -*-  
from sqlalchemy import create_engine

def get_db_connect():
    conn = create_engine('postgresql://postgres:142857@47.93.193.128:5432/tushare')
    return conn

