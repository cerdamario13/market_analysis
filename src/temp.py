import requests
import os
import pandas as pd

secret_key = os.environ.get('ALPHAV_KEY', '...')

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=AAPL&interval=60min&apikey={secret_key}'
r = requests.get(url)
data = r.json()

df = pd.DataFrame.from_dict(data)
print(df.to_markdown())

print()
