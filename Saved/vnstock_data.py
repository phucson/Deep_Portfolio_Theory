'''
13/12/2023
    out of memory when combine_tickers
'''
import pandas as pd
import numpy as np

from vnstock import stock_historical_data

from utils import load_tickers, combine_tickers


start_train = '2019-1-1'
end_train = '2021-1-1'

start_val = '2021-1-2'
end_val = '2023-12-12'

vn30 = ['ACB', 'BCM', 'BID', 'BVH', 'CTG',
        'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
        'MBB', 'MSN', 'MWG', 'PLX', 'POW',
        'SAB', 'SHB', 'SSI', 'STB', 'TCB',
        'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
        'VJC', 'VNM', 'VPB', 'VRE', 'SSB']

ten = np.random.choice(vn30, size=20)

l = load_tickers(vn30, start_train, end_val)

res = pd.DataFrame({'time': pd.date_range(start_train, end_val)})
date_range = res['time']
cols = ['time', 'close', 'return']

for i in range(len(vn30)):
    tic = l[i].ticker.iloc[0]
    temp = l[i][cols].rename(columns={'close': f'close_{tic}',
                              'return': f'return_{tic}'}).drop_duplicates('time')
    res = res.merge(temp,
                    on='time',
                    how='left')

df = combine_tickers(l, start_train, end_val)

