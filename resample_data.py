import pandas as pd

data_folder = './data/'
index_file = 'vni.csv'

start_train = '2019-1-15'
end_train = '2021-1-1'

start_val = '2021-1-2'
end_val = '2023-12-17'

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

ind = pd.read_csv(data_folder+index_file, 
                  parse_dates=['Date'],
                  index_col='Date').sort_index(ascending=True)

ind['Change'] = ind['Price'].diff()
ind.rename(columns={'Change %':'% Change'})
ind = ind.rename(columns={'Price':"PX_LAST"}).dropna()
ind['Change %'] = ind['Change %'].str.replace('%', '').astype('float')
ind['Change %'] = ind['Change %'].div(100)

last_price = pd.read_csv('./daily_data/last_price.csv', 
                  parse_dates=['date'],
                  index_col='date')
last_price_w = last_price.resample("W").mean().ffill()


net_change_w = last_price_w.diff().ffill().fillna(0)

pct_change_w = last_price_w.pct_change().ffill().fillna(0)

ind.to_csv(data_folder+'vni.csv')
last_price_w.to_csv(data_folder+'last_price.csv')
net_change_w.to_csv(data_folder+'net_change.csv')
pct_change_w.to_csv(data_folder+'percentage_change.csv')
