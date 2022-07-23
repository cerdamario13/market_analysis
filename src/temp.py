import func

ticker = 'AAPL'
    
# Dataframe with all the data
data = func.ticker_data_all(ticker)

# Testings X month ago - works for years too
one_month = func.x_month_ago(data, 60, 'Close')
two_month = func.x_month_ago(data, 5, 'Close')


# TODO Add ago functions
# 5 days, 6 months, year to date, 1 year, 5 year, max
print()