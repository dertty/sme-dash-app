import numpy as np
import pandas as pd
from datetime import datetime as dt

class DataProvider:
    def __init__(self):
        self.portfolio_data_ = pd.read_excel('data/data.xlsx')


    def GetDatesFilterBounds(self):
        return dt(2018, 1, 1), dt(2020, 10, 1)

    def GetCountsData(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None, product_decompose=False):
        data = self.portfolio_data_
        if checked_loan_types:
            data = data[data['credit_type'].isin(checked_loan_types)]
        if checked_default_types:
            data = data[data['default_reason'].isin(checked_default_types + [None, ])]
        if start_date:
            data = data[data['report_dt'] >= start_date]
        if end_date:
            data = data[data['report_dt'] < end_date]

        if product_decompose:
            result = data.groupby(by=['report_dt','cred_type'])['id'].count()
        else:
            result = data.groupby(by='report_dt')['id'].count()

        return result