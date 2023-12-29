import pandas as pd

import numpy as np

earliest = pd.to_datetime('2018-5-18', format="%Y-%m-%d")

tickers = ['HDB', 'MBB', 'JVC', 'ACB', 'VND',
           'PVT', 'AAA', 'TPB', 'HAH',
           'VHM', 'VNM', 'VHC', 'PNJ', 'BVH',
           'GAS', 'BCM', 'FRT', 'SAB', 'DHG',
           'VIC', 'VJC', 'MSN', 'SLS', 'RAL',
           'DBC', 'PTB', 'OGC', 'KPF', 'DRC',
           'DAH']

suff = " Historical Data.csv"

for i, tic in enumerate(tickers):
    filename = tic+suff
    temp = pd.read_csv(filename, index_col=False)
    temp['Date'] = pd.to_datetime(temp['Date'], format="%m/%d/%Y")

    if i == 0:
        res = temp[['Date', 'Price']]
        res = res.rename(columns={'Price':tic})
    else:
        res = res.merge(temp[['Date', 'Price']], on="Date", how='left')
        res = res.rename(columns={'Price':tic})

res = res[res.Date >= earliest]
res = res.sort_values('Date').ffill()
res = res.set_index('Date')

for i, col in enumerate(res.columns):
    res[col] = res[col].str.replace(',', '').astype('float')

res.to_csv('res.csv')
