import pandas_datareader as pdr
from datetime import datetime
import pandas as _pd
import dateutil.relativedelta

# latest stock info
def simple_data(ticker:str) -> list:
    fund = pdr.get_data_yahoo(ticker)['Close'][-1]
    return round(fund, 2)
    
# Get all of the data loaded
def ticker_data_all(ticker:str) -> _pd.DataFrame:
    fund = pdr.get_data_yahoo(ticker)
    fund.reset_index(inplace=True)

    return fund
    

def date_range_data(start_date: str, end_date: str, ticker: str) -> _pd.DataFrame:

    start_date_format = datetime.strptime(start_date, "%m/%d/%Y")
    end_date_format = datetime.strptime(end_date, "%m/%d/%Y")

    # Getting the first (date) element of the data and comparing with function end data
    # first_date = ticker_data_all(ticker)['Date'].iloc[0]

    mask =  (end_date_format > ticker_data_all(ticker)['Date']) & (start_date_format < ticker_data_all(ticker)['Date'])

    return ticker_data_all(ticker)[mask]


def annual_rate_return(star_date: str, end_date: str, data: _pd.DataFrame)-> float:

    df = data

    # Grouping the list into years
    df['Year'] = _pd.DatetimeIndex(df['Date']).year
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


# X month ago calculator
def x_month_ago(data: _pd.DataFrame, month: int = 1, value: str = 'Close') -> _pd.DataFrame:
    
    df = data

    today = datetime.today()
    
    # Testing Dates
    # date_str = '2022-06-30'
    # today = datetime.strptime(date_str, "%Y-%m-%d")
    m_1 = today - dateutil.relativedelta.relativedelta(months=month) # subtract one month
        
    # If the day falls on Sunday, add a day
    if m_1.weekday() == 6:
        m_1 = m_1 + dateutil.relativedelta.relativedelta(days=1)
    elif m_1.weekday() == 5: # If saturday, add two days
        m_1 = m_1 + dateutil.relativedelta.relativedelta(days=2)
        
    mask1 = df['Date'] == m_1.strftime("%Y-%m-%d")
    
    # Dealing with market closures M_1
    count = 0
    while (df[mask1].empty):
        m_1 = m_1 + dateutil.relativedelta.relativedelta(days=1)
        mask1 = df['Date'] == m_1.strftime("%Y-%m-%d")
        count += 1

        # Safety break
        if count == 10:
            raise ValueError('An unexpected error ocurred. Try again.')
        
    # New mask
    mask1 = df['Date'] >= m_1.strftime("%Y-%m-%d")
    return df[mask1]







    

    

    

    



