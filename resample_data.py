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

ind = pd.read_csv(index_file, 
                  parse_dates=['date'],
                  index_col='date')
ind_w = ind.resample("W").mean().ffill()

last_price = pd.read_csv('last_price.csv', 
                  parse_dates=['date'],
                  index_col='date')
last_price_w = last_price.resample("W").mean().ffill()


net_change = pd.read_csv('net_change.csv', 
                  parse_dates=['date'],
                  index_col='date')
net_change_w = net_change.resample("W").mean().ffill()

pct_change = pd.read_csv('percentage_change.csv', 
                  parse_dates=['date'],
                  index_col='date')
pct_change_w = pct_change.resample("W").mean().ffill()

ind_w.to_csv(data_folder+'vni.csv')
last_price_w.to_csv(data_folder+'last_price.csv')
net_change_w.to_csv(data_folder+'net_change.csv')
pct_change_w.to_csv(data_folder+'pct_change.csv')
