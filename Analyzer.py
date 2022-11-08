import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re

class MarketDB:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root',
            password='1111', db='INVESTAR', charset='utf8')
        self.codes = {}
        self.get_comp_info()

    def __del__(self):
        self.conn.close()

    # company_info 테이블에서 읽어와서 codes에 저장
    def get_comp_info(self):
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]
            
    def get_daily_price(self, code, start_date=None, end_date=None):
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())
        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")
        sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
            f" and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df