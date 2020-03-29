import numpy as np
import pandas as pd
from datetime import datetime as dt


class DataProvider:
    def __init__(self):
        self.portfolio_data_ = pd.read_excel('data/data.xlsx')
        self.product_types_ = self.portfolio_data_['credit_type'].unique()
        self.default_reasons_ = self.portfolio_data_['default_reason'].dropna().unique()

    def _getFilteredData(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None):
        data = self.portfolio_data_
        if checked_loan_types:
            data = data[data['credit_type'].isin(checked_loan_types)]
        if checked_default_types:
            data = data[data['default_reason'].isin(checked_default_types + [None, ])]
        if start_date:
            data = data[data['report_dt'] >= start_date]
        if end_date:
            data = data[data['report_dt'] < end_date]

        return data


    @property
    def GetProductTypes(self):
        """
        Возвращает полный список продуктов
        :return: Список продуктов
        """
        return self.product_types_

    @property
    def GetDefaultReasons(self):
        """
        Возвращает полный список причин дефолта
        :return: Список причин дефолта
        """
        return self.default_reasons_

    @property
    def GetDatesBounds(self):
        """
        Возвращает минимальную и максимлаьную дату наблюдений
        :return: Минимальная и максимлаьная дата наблюдений
        """
        #TODO: Извлекать дату в конструкте и тут возвращать
        return dt(2018, 1, 1), dt(2020, 10, 1)

    def GetDefaultsCount(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None):
        """
        Возвращает число дефолтов, подходящих по критериям
        :return: число дефолтов, подходящих по критериям
        """
        data = self._getFilteredData(start_date, end_date, checked_default_types, checked_loan_types)
        default_count = data['cur_default'].sum()
        return default_count

    def GetDR(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None):
        """
        Возвращает DR подходящих по критериям наблюдений
        :return: DR подходящих по критериям наблюдений
        """
        data = self._getFilteredData(start_date, end_date, checked_default_types, checked_loan_types)
        dr = data['default_12m'].sum() / data.shape[0]
        return dr

    def GetCount(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None):
        """
        Возвращает число подходящих по критериям наблюдений
        :return: Число подходящих по критериям наблюдений
        """
        data = self._getFilteredData(start_date, end_date, checked_default_types, checked_loan_types)
        return data.shape[0]



    def GetCountsData(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None,
                      product_decompose=False):
        data = self._getFilteredData(start_date, end_date, checked_default_types, checked_loan_types)

        if product_decompose:
            result = data.groupby(by=['report_dt', 'cred_type'])['id'].count()
        else:
            result = data.groupby(by='report_dt')['id'].count()
        return result

    def GetRatingData(self, start_date=None, end_date=None, checked_default_types=None, checked_loan_types=None,
                      product_decompose=False):
        data = self._getFilteredData(start_date, end_date, checked_default_types, checked_loan_types)

        result = data.groupby(by='rating').size()
        return result