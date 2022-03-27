
import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import dateutil.relativedelta


def ticker_data_all(ticker:str = 'GOOG'):
    fund = pdr.get_data_yahoo(ticker)
    fund.reset_index(inplace=True)

    return fund


