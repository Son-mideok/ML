# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:56:43 2022

@author: virtue
"""

import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user = 'root',
            password='1111', db='INVESTAR', charset='utf8')
        self.codes = {}
        self.get_comp_info()
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()


    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]
        print(krx)
 
    def get_daily_price(self, code, start_date=None, end_date=None):
       codes_keys = list(self.codes.keys())
       codes_values = list(self.codes.values())
       print(codes_keys)

       if code in codes_keys:
           pass
       elif code in codes_values:
           idx = codes_values.index(code)
           print(idx)

           code = codes_keys[260]
           print(code)
       else:
           print(f"ValueError: Code({code}) doesn't exist.")

       sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
           f" and date >= '{start_date}' and date <= '{end_date}'"
       df = pd.read_sql(sql, self.conn)
       df.index = df['date']
       return df


mk = MarketDB()

raw_df = mk.get_daily_price('삼성전자', '2020-01-01', '2021-12-10')
print(raw_df)