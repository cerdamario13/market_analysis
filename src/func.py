
import pandas_datareader as pdr
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def ticker_data_all(ticker:str):
    fund = pdr.get_data_yahoo(ticker)
    fund.reset_index(inplace=True)

    return fund

def date_range_data(start_date: str, end_date: str, ticker: str) -> pd.DataFrame:

    start_date_format = datetime.strptime(start_date, "%m/%d/%Y")
    end_date_format = datetime.strptime(end_date, "%m/%d/%Y")

    # Getting the first (date) element of the data and comparing with function end data
    first_date = ticker_data_all(ticker)['Date'].iloc[0]

    if end_date_format < first_date:
        end_date_format = first_date

    mask =  (start_date_format < ticker_data_all(ticker)['Date']) & (end_date_format > ticker_data_all(ticker)['Date'])

    return ticker_data_all(ticker)[mask]

# print(date_range_data('3/20/2000', '3/27/2022', 'AAPL'))

def annual_rate_return(star_date: str, end_date: str, ticker: str)-> float:

    df = date_range_data(star_date, end_date, ticker)

    # Grouping the list into years
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    years = df.groupby('Year')
    list_years = list(years.groups.keys())

    # Yearly rate of return since beginning
    yrr = []
    for x in list_years:
        a = years.get_group(x).iloc[0]['Close']
        b = years.get_group(x).iloc[-1]['Close']
        y = ((b - a) / a) * 100
        yrr.append(y)

    #Average Rate of Return
    arr = sum(yrr) / len(yrr)
    return round(arr, 2)

# print(annual_rate_return('1/1/2020', '3/13/2022', 'AAPL'))



    

    

    

    



