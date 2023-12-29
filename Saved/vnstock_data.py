import pandas as pd
import numpy as np

from vnstock import stock_historical_data

from utils import load_tickers, combine_tickers

data_folder = './data/'
index_file = 'vn30.csv'

start_train = '2019-1-14'
end_train = '2021-1-1'

start_val = '2021-1-2'
end_val = '2023-12-17'

vn30 = ['ACB', 'BCM', 'BID', 'BVH', 'CTG',
        'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
        'MBB', 'MSN', 'MWG', 'PLX', 'POW',
        'SAB', 'SHB', 'SSI', 'STB', 'TCB',
        'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
        'VJC', 'VNM', 'VPB', 'VRE', 'SSB']

vn29 = ['ACB', 'BCM', 'BID', 'BVH', 'CTG',
        'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
        'MBB', 'MSN', 'MWG', 'PLX', 'POW',
        'SAB', 'SHB', 'SSI', 'STB', 'TCB',
        'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
        'VJC', 'VNM', 'VPB', 'VRE']


additional = ['DGC', 'KBC', 'KDH', 'VND', 'DPM',
              'PVC', 'CLC', 'DPR', 'DHG', 'PHR',
              'PVS', 'SLS', 'VNG', 'SBT', 'EIB',
              'LAS', 'FCN', 'PXS', 'DMC', 'BMP',
              'PVD', 'JVC', 'DVP', 'KDC', 'NSC',
              'DCM', 'AAA', 'DAH', 'MPC', 'SCS',
              'TLG', 'REE', 'GEG', 'RAL', 'MSH',
              'VHC', 'PNJ', 'LTG', 'FRT', 'DBC',
              'HAH', 'HHV', 'NBB', 'ITA', 'NVL',
              'BCG', 'ANV', 'CII', 'GEX', 'BWE',
              'PC1', 'SKG', 'BMC', 'HCM']

vn83 = list(set(vn29).union(additional))
len(vn83)

dup = {x for x in additional if additional.count(x)>1}

l = load_tickers(vn83, start_train, end_val)

vni = pd.read_csv(data_folder+'vni.csv', index_col=False)[['date', 'close']]
vni['date'] = pd.to_datetime(vni['date'], format="%d/%m/%Y")
vni = vni.sort_values('date')

last_price = pd.DataFrame({'time': vni['date']})
net_change = pd.DataFrame({'time': vni['date']})
percentage_change = pd.DataFrame({'time': vni['date']})

cols = ['time', 'close']

for i in range(len(vn83)):
    tic = l[i].ticker.iloc[0]

    price = l[i][cols].rename(columns={'close': f'{tic}'}).drop_duplicates('time')
    print(f'{tic} NA: {price.isna().sum()}')
    last_price = last_price.merge(price,
                    on='time',
                    how='left')
    
    net = l[i][['time', 'return']].rename(columns={'return':f'{tic}'}).drop_duplicates('time')
    net_change = net_change.merge(net,
                                  on='time',
                                  how='left')

    pct = l[i][['time']].drop_duplicates()
    pct[f'{tic}'] = price[f'{tic}'].pct_change()
    percentage_change = percentage_change.merge(pct,
                                                on='time',
                                                how='left')

last_price.isna().sum().sort_values(ascending=False)
net_change.isna().sum().sort_values(ascending=False)
percentage_change.isna().sum().sort_values(ascending=False)

last_price = last_price.ffill().dropna().rename(columns={'time':'date'})
last_price = last_price.iloc[1:, :]

net_change.ffill().dropna().rename(columns={'time':'date'})
net_change = net_change.iloc[1:, :]

percentage_change.ffill().dropna().rename(columns={'time':'date'})
percentage_change = percentage_change.iloc[1:, :]

last_price.to_csv('last_price.csv', index=False)
net_change.to_csv('net_change.csv', index=False)
percentage_change.to_csv('percentage_change.csv', index=False)
vni.to_csv('vni.csv', index=False)